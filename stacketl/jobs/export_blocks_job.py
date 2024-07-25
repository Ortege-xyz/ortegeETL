import json
import logging
from typing import List
from stacketl.api.stack_api import StackApi
from stacketl.domain.block import StackBlock
from stacketl.domain.contract import StackContract
from stacketl.domain.transaction import StackTransaction
from stacketl.mappers.block_mapper import StackBlockMapper
from stacketl.mappers.contract_mapper import StackContractMapper
from stacketl.mappers.transaction_mapper import StackTransactionMapper
from stacketl.service.stack_contract_service import StackContractService
from blockchainetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from blockchainetl.utils import validate_range
from blockchainetl.classes.base_item_exporter import BaseItemExporter


# Exports blocks and transactions and contracts
class ExportBlocksJob(BaseJob):
    def __init__(
            self,
            start_block: int,
            end_block: int,
            batch_size: int,
            stack_api: StackApi,
            max_workers: int,
            item_exporter: BaseItemExporter,
            export_blocks=True,
            export_transactions=True,
            export_contracts=True):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.export_blocks = export_blocks
        self.export_transactions = export_transactions
        self.export_contracts = export_contracts
        if not self.export_blocks and not self.export_transactions and not self.export_contracts:
            raise ValueError('At least one of export_blocks or export_transactions or export_contracts must be True')

        self.stack_api = stack_api
        self.block_mapper = StackBlockMapper()
        self.transaction_mapper = StackTransactionMapper()
        self.contract_mapper = StackContractMapper()
        self.contract_service = StackContractService()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_batch,
            total_items=self.end_block - self.start_block + 1
        )

    def _export_batch(self, block_number_batch: List[int]):
        blocks = self.stack_api.get_blocks(block_number_batch)

        if self.export_transactions or self.export_contracts:
            transactions = self.stack_api.get_blocks_transactions(block_number_batch, self.export_transactions)
            
            if self.export_transactions:
                for block, transaction in zip(blocks, transactions):
                    if block and transaction:
                        block.transactions = transactions
                        self._export_block(block)
            
            if self.export_contracts:
                def filter_deploy_contracts_txs(transaction: StackTransaction) -> bool:
                    return transaction.tx_type == "smart_contract" and transaction.tx_status == "success"

                txs_contract: List[StackTransaction] = list(filter(filter_deploy_contracts_txs, transactions))

                if(len(txs_contract) == 0):
                    return

                contracts_ids = [tx_contract.smart_contract["contract_id"] for tx_contract in txs_contract]
                contracts_results = self.stack_api.get_contracts_infos(contracts_ids)

                for contract_result in contracts_results:
                    if contract_result is None or contract_result.abi is None: # https://github.com/hirosystems/stacks-blockchain-api/issues/1848
                        logging.warning(f"Error: The abi of the contract {contract_result.address} is null, skipping this contract.")
                        continue
                    contract = self._get_contract(contract_result)
                    self.item_exporter.export_item(self.contract_mapper.contract_to_dict(contract))

            return

        for block in blocks:
            if block:
                self._export_block(block)

    def _export_block(self, block: StackBlock):
        if self.export_blocks:
            self.item_exporter.export_item(self.block_mapper.block_to_dict(block))

        if self.export_transactions:
            for tx in block.transactions:
                self.item_exporter.export_item(self.transaction_mapper.transaction_to_dict(tx))

    def _get_contract(self, contract: StackContract):
        abi = json.loads(contract.abi)

        def extract_function_name(item) -> str:
            return item['name']

        functions = list(map(extract_function_name, abi["functions"]))

        contract.is_stx20 = self.contract_service.is_stx20_contract(functions)
        contract.is_nft = self.contract_service.is_nft_contract(functions)

        return contract

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
