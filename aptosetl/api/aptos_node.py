from typing import Any, Dict, List

from aptosetl.domain.block import AptosBlock
from aptosetl.domain.transaction import AptosTransaction
from blockchainetl.api_requester import ApiRequester

TRANSACTION_LIMIT = 100

GET_BLOCK_BY_NUMBER = 'v1/blocks/by_height/{block_number}'
GET_TRANSACTIONS = 'v1/transactions'
GET_TRANSACTION_BY_HASH = 'v1/transactions/by_hash/{txn_hash}'
GET_LEDGER_INFO = 'v1/'

class AptosNodeApi(ApiRequester):
    """
        Class to fetch data from Aptos blockchain
        See more in https://fullnode.devnet.aptoslabs.com/v1/spec#/
    """
    def __init__(self, api_url: str):
        rate_limit = 15 # 15 request per second https://aptos.dev/apis/fullnode-rest-api/#understanding-rate-limitsre

        super().__init__(api_url, api_key=None, rate_limit=rate_limit)

        self.headers = {
            'Accept': 'application/json'
        }

    def get_latest_block(self) -> int:
        """Get the last block number"""
        response = self._make_get_request(GET_LEDGER_INFO, headers=self.headers)

        data = response.json()

        return int(data['block_height'])

    def get_block(self, block_number: int, with_transactions: bool = False) -> Dict[str, Any]:
        """Get the block by the number"""
        params = {
            'with_transactions': str(with_transactions).lower()
        }

        response = self._make_get_request(
            endpoint=GET_BLOCK_BY_NUMBER.format(block_number=block_number),
            headers=self.headers,
            params=params,
        )

        return response.json()

    def get_block_transactions(self, block_number: int) -> List[Dict[str, Any]]:
        block = self.get_block(block_number, True)

        return block["transactions"]

    def get_blocks(self, blocks_numbers: List[int], with_transactions: bool = False):
        """Get all blocks by the numbers"""
        blocks: List[AptosBlock] = []
        for block_dict in self._generate_blocks(blocks_numbers, with_transactions):
            block = AptosBlock.from_dict(block_dict)
            if with_transactions:
                for transaction in block_dict['transactions']:
                    transaction['block_number'] = block.number
                    block.transactions.append(AptosTransaction.from_dict(transaction))
            blocks.append(block)
            
        return blocks

    def get_blocks_transactions(self, blocks_numbers: List[int]):
        """Get all block transactions by numbers"""
        transactions: List[List[AptosTransaction]] = []
        for transactions_result in self._generate_blocks_transactions(blocks_numbers):
            txs = []
            for transaction in transactions_result:
                txs.append(AptosTransaction.from_dict(transaction))
            transactions.append(txs)

        return transactions

    def _generate_blocks(self, blocks_numbers: List[int], with_transactions: bool = False):
        for block_number in blocks_numbers:
            yield self.get_block(block_number, with_transactions)

    def _generate_blocks_transactions(self, blocks_numbers: List[int]):
        for block_number in blocks_numbers:
            yield self.get_block_transactions(block_number)
