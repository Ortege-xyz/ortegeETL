import requests
from typing import Any, Optional

from stacketl.mappers.block_mapper import StackBlockMapper
from stacketl.mappers.transaction_mapper import StackTransactionMapper
from stacketl.domain.block import StackBlock
from stacketl.domain.transaction import StackTransaction

TRANSACTION_LIMIT = 50

GET_BLOCK_PATH = 'extended/v1/block/by_height/{number}'
GET_BLOCK_TRANSACTIONS_PATH = 'extended/v1/tx/block_height/{number}'
GET_TRANSACTION_PATH = 'extended/v1/tx/{hash}'

class StackApi():
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.block_mapper = StackBlockMapper()
        self.transaction_mapper = StackTransactionMapper()

    def get_block(self, block_number: int) -> Optional[dict[str, Any]]:
        """Get the block by the number"""
        url = self.api_url + GET_BLOCK_PATH.format(number=block_number)

        response = requests.get(url)

        if str(response.status_code).startswith(('4', '5')):
            return None
        
        return response.json()
    
    def get_block_transactions(self, block_number: int) -> Optional[dict[str, Any]]:
        """Get all block transactions by the number"""
        url = self.api_url + GET_BLOCK_TRANSACTIONS_PATH.format(number=block_number)

        params = {
            'limit': TRANSACTION_LIMIT,
            'offset': 0,
        }

        # if str(response.status_code).startswith(('4', '5')):
        #     return None
        transactions = []
        while True:
            response = requests.get(url, params=params)
            data = response.json()
            
            transactions.extend(data['results'])

            if data['total'] > TRANSACTION_LIMIT:
                params['offset'] = params['offset'] + TRANSACTION_LIMIT
            else:
                break

            if transactions >= data['total']:
                break

        return transactions

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

    def _generate_blocks(self, blocks_numbers: list[int]):
        for block_number in blocks_numbers:
            yield self.get_block(block_number)

    def _generate_blocks_transactions(self, blocks_numbers: list[int]):
        for block_number in blocks_numbers:
            yield self.get_block_transactions(block_number)
            