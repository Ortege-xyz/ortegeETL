from typing import Any, Optional

from sorobanetl.domain.block import SorobanBlock
from sorobanetl.domain.transaction import SorobanTransaction
from blockchainetl.api_requester import ApiRequester

TRANSACTION_LIMIT = 200

GET_LAST_LEDGER= 'ledger?order=desc&limit=1'
GET_LEDGER = 'ledgers/{number}'
GET_LEDGER_TRANSACTIONS_PATH = '/ledgers/{number}/transactions'
GET_TRANSACTION_PATH = 'transactions/{tx_id}'


class HorizonApi(ApiRequester):
    """
        Class to fetch data from Stellar blockchain via Horizon api
        See more in https://developers.stellar.org/api/horizon
    """
    def __init__(self, api_url: str):
        rate_limit = 1 # 1 request per second

        super().__init__(api_url, rate_limit=rate_limit)

        self.headers = {
            'Accept': 'application/json'
        }

    def get_latest_ledger(self) -> SorobanBlock:
        """Get the last ledger"""
        response = self._make_get_request(GET_LAST_LEDGER, headers=self.headers, timeout=2)

        data = response.json()

        return self.block_mapper.json_dict_to_block(data["results"][0])

    def get_ledger(self, ledger_number: int) -> Optional[dict[str, Any]]:
        """Get the ledger by the number"""
        response = self._make_get_request(
            endpoint=GET_LEDGER.format(number=ledger_number),
            headers=self.headers,
            timeout=2
        )

        return response.json()

    def get_ledger_transactions(self, ledger_number: int) -> list[dict[str, Any]]:
        """Get all ledger transactions by the number"""
        transactions = []
        url = GET_LEDGER_TRANSACTIONS_PATH.format(number=ledger_number) + f'?limit={TRANSACTION_LIMIT}&order=asc'

        while True:
            response = self._make_get_request(
                endpoint=url,
                headers=self.headers,
                timeout=2,
            )
            data = response.json()

            url = data['_links']['next']['href']

            txs = data['_embedded']['records']

            if len(txs) == 0:
                break

            transactions.extend(txs)

        return transactions

    def get_blocks(self, ledgers_numbers: list[int]):
        """Get all blocks by the numbers"""
        blocks: list[Optional[SorobanBlock]] = []
        for ledger_detail_result in self._generate_ledgers(ledgers_numbers):
            if ledger_detail_result:
                blocks.append(SorobanBlock.json_dict_to_block(ledger_detail_result))
            
        return blocks

    def get_ledgers_transactions(self, ledgers_numbers: list[int]):
        """Get all ledger transactions by numbers"""
        transactions: list[Optional[SorobanTransaction]] = []
        for ledger_transactions_result in self._generate_ledgers_transactions(ledgers_numbers):
            for transaction in ledger_transactions_result:
                if transaction:
                    transactions.append(SorobanTransaction.json_dict_to_block(transaction))

        return transactions

    def _generate_ledgers(self, ledgers_numbers: list[int]):
        for ledger_number in ledgers_numbers:
            yield self.get_ledger(ledger_number)

    def _generate_ledgers_transactions(self, ledgers_numbers: list[int]):
        for ledger_number in ledgers_numbers:
            yield self.get_ledger_transactions(ledger_number)
