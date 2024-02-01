import json
import logging

from blockchainetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from blockchainetl.utils import validate_range
from stacketl.domain.contract import StackContract
from stacketl.domain.transaction import StackTransaction
from stacketl.mappers.contract_mapper import StackContractMapper
from stacketl.mappers.transaction_mapper import StackTransactionMapper
from stacketl.api.stack_api import StackApi
from stacketl.service.stack_contract_service import StackContractService


# Exports contracts bytecode
class ExportContractsJob(BaseJob):
    def __init__(
            self,
            start_block: int,
            end_block: int,
            batch_size: int,
            stack_api: StackApi,
            max_workers,
            item_exporter):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.stack_api = stack_api
        self.contract_service = StackContractService()
        self.contract_mapper = StackContractMapper()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_contracts,
            total_items=self.end_block - self.start_block + 1
        )

    def _export_contracts(self, block_number_batch: list[int]):
        transactions = self.stack_api.get_blocks_transactions(block_number_batch)

        def filter_contracts(transaction: StackTransaction) -> bool:
            return transaction.tx_type == "smart_contract" and transaction.tx_status == "success"

        txs_contract: list[StackTransaction] = list(filter(filter_contracts, transactions))

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
