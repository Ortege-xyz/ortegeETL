import requests
from typing import Any, Optional

from stacketl.mappers.block_mapper import StackBlockMapper
from stacketl.mappers.contract_mapper import StackContractMapper
from stacketl.mappers.transaction_mapper import StackTransactionMapper
from stacketl.domain.block import StackBlock
from stacketl.domain.contract import StackContract
from stacketl.domain.transaction import StackTransaction
from blockchainetl.api_requester import ApiRequester

TRANSACTION_LIMIT = 50

GET_BLOCK_PATH = 'extended/v2/blocks/{number}'
GET_BLOCK_TRANSACTIONS_PATH = 'extended/v2/blocks/{number}/transactions'
GET_CONTRACT_INFO_PATH = 'extended/v1/contract/{contract_id}'
GET_LAST_BLOCK_PATH = 'extended/v2/blocks?limit=1'
GET_TRANSACTION_PATH = 'extended/v1/tx/{hash}'

class StackApi(ApiRequester):
    def __init__(self, api_url: str, api_key: Optional[str]):
        if api_key:
            rate_limit = 500/60 # 500 request per minutes, the value should be requests per seconds
        else:
            rate_limit = 50/60 # 50 request per minutes

        super().__init__(api_url, api_key, rate_limit)

        self.block_mapper = StackBlockMapper()
        self.contract_mapper = StackContractMapper()
        self.transaction_mapper = StackTransactionMapper()

        if self.api_key:
            self.headers = {
                'x-hiro-api-key': self.api_key
            }
        else:
            self.headers = None

    def get_latest_block(self) -> StackBlock:
        """Get the last block"""
        response = self._make_get_request(GET_LAST_BLOCK_PATH, headers=self.headers, timeout=2)

        data = response.json()

        return self.block_mapper.json_dict_to_block(data["results"][0])

    def get_block(self, block_number: int) -> Optional[dict[str, Any]]:
        """Get the block by the number"""
        response = self._make_get_request(
            endpoint=GET_BLOCK_PATH.format(number=block_number),
            headers=self.headers,
            timeout=2
        )

        if str(response.status_code).startswith(('4', '5')):
            return None
        
        return response.json()
    
    # TODO: update to new endpoint https://docs.hiro.so/api/get-transactions-by-block
    def get_block_transactions(self, block_number: int) -> list[dict[str, Any]]:
        """Get all block transactions by the number"""
        params = {
            'limit': TRANSACTION_LIMIT,
            'offset': 0,
        }

        transactions = []
        while True:
            response = self._make_get_request(
                endpoint=GET_BLOCK_TRANSACTIONS_PATH.format(number=block_number),
                params=params,
                headers=self.headers,
                timeout=2,
            )
            data = response.json()
            
            transactions.extend(data['results'])
            if data['total'] > TRANSACTION_LIMIT:
                params['offset'] = params['offset'] + TRANSACTION_LIMIT
            else:
                break

            if len(transactions) >= data['total']:
                break

        return transactions

    def get_contract_info(self, contract_id: str) -> Optional[dict[str, Any]]:
        response = self._make_get_request(
            endpoint=GET_CONTRACT_INFO_PATH.format(contract_id=contract_id),
            headers=self.api_key,
            timeout=2
        )

        if str(response.status_code).startswith(('4', '5')):
            return None

        return response.json()

    def get_blocks(self, blocks_numbers: list[int]):
        """Get all blocks by the numbers"""
        blocks: list[Optional[StackBlock]] = []
        for block_detail_result in self._generate_blocks(blocks_numbers):
            if block_detail_result:
                blocks.append(self.block_mapper.json_dict_to_block(block_detail_result) if block_detail_result is not None else block_detail_result)
            
        return blocks

    def get_blocks_transactions(self, blocks_numbers: list[int]):
        """Get all block transactions by numbers"""
        transactions: list[Optional[StackTransaction]] = []
        for block_transactions_result in self._generate_blocks_transactions(blocks_numbers):
            for transaction in block_transactions_result:
                if block_transactions_result:
                    transactions.append(self.transaction_mapper.json_dict_to_transaction(transaction) if transaction is not None else transaction)

        return transactions

    def get_contracts_infos(self, contracts_ids: list[str]):
        contracts: list[StackContract] = []
        for contract_result in self._generate_get_contracts_info(contracts_ids):
            if contract_result:
                contracts.append(self.contract_mapper.json_dict_to_contract(contract_result))

        return contracts

    def _generate_blocks(self, blocks_numbers: list[int]):
        for block_number in blocks_numbers:
            yield self.get_block(block_number)

    def _generate_blocks_transactions(self, blocks_numbers: list[int]):
        for block_number in blocks_numbers:
            yield self.get_block_transactions(block_number)
    
    def _generate_get_contracts_info(self, contracts_ids: list[str]):
        for contract_id in contracts_ids:
            yield self.get_contract_info(contract_id)
