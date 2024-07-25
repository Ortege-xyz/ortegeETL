import logging
from typing import Any, Dict, List, Optional

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
GET_LIST_OF_TRANSACTIONS_PATH = 'extended/v1/tx/multiple?{transactions}'
GET_CURRENT_POX_PATH = 'v2/pox'

class StackApi(ApiRequester):
    def __init__(self, api_url: str, api_key: Optional[str]):
        if api_key:
            rate_limit = 490/60 # 490 request per minutes, the value should be requests per seconds
        else:
            rate_limit = 45/60 # 45 request per minutes

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
        response = self._make_get_request(GET_LAST_BLOCK_PATH, headers=self.headers, timeout=4)

        try:
            data = response.json()
            block = self.block_mapper.json_dict_to_block(data["results"][0])
        except Exception as e:
            logging.warn(f"Error in get last block, status {response.status_code} \n {response.text}")
            raise e
        return block

    def get_block(self, block_number: int) -> Optional[Dict[str, Any]]:
        """Get the block by the number"""
        response = self._make_get_request(
            endpoint=GET_BLOCK_PATH.format(number=block_number),
            headers=self.headers,
            timeout=4
        )

        if str(response.status_code).startswith(('4', '5')):
            return None
        
        return response.json()
    
    def get_block_transactions(self, block_number: int) -> List[Dict[str, Any]]:
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
                timeout=4,
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

    def get_details_transactions(self, transactions: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get the details of a list of transactions"""
        transactions = list(map(lambda tx: "tx_id="+tx, transactions))

        transaction_mapping: Dict[str, Dict[str, Any]] = {}

        params = {
            'event_limit': 50,
            'event_offset': 0,
        }

        def get_transactions(_transactions: List[str]):
            _transactions_mapping = {}
            # split the list in 40 elements to make the requets
            for i in range(0, len(_transactions), 40):

                url = GET_LIST_OF_TRANSACTIONS_PATH.format(transactions="&".join(_transactions[i:i + 40]))
                reponse = self._make_get_request(
                    endpoint=url,
                    headers=self.headers,
                    timeout=4,
                    params=params
                )

                data = reponse.json()
                _transactions_mapping.update(data)
            return _transactions_mapping

        transaction_mapping.update(get_transactions(transactions))

        # some transactions have a mismatch of the event_count with the lenght of events array
        # for example tx 0x45d7d56659be739cb2fae927dc119f3c4267011210736ce29a162a956be8f586 only return 33 events and have the event_count 85
        finished_transactions = {}
        def filter_txs(tx: Dict[str, Any]):
            tx_hash = tx["result"].get('tx_id', '')
            event_count = tx["result"].get('event_count', 0)
            events = tx["result"].get('events', [])
            return event_count > 50 and event_count != len(events) and finished_transactions.get(tx_hash, False) is False

        event_offset_index = 1
        while True:
            # get the events of transactions with more than 50 events
            transactions_missing_events = list(
                map(
                    lambda tx: "tx_id="+tx["result"]["tx_id"],
                    filter(
                        filter_txs,
                        transaction_mapping.values()
                    )
                )
            )

            if(len(transactions_missing_events) == 0):
                break

            params["event_offset"] = event_offset_index * 50
            event_offset_index += 1

            transactions_missing_events_mapping = get_transactions(transactions_missing_events)

            # Update the transactions with the events
            for transaction in transactions_missing_events_mapping.values():
                transaction_hash: str = transaction["result"]["tx_id"]
                transaction_events = transaction["result"]["events"]

                if len(transaction_events) == 0:
                    finished_transactions[transaction_hash] = True

                transaction_mapping[transaction_hash]["result"]["events"].extend(transaction_events)

        return transaction_mapping

    def get_contract_info(self, contract_id: str) -> Optional[Dict[str, Any]]:
        response = self._make_get_request(
            endpoint=GET_CONTRACT_INFO_PATH.format(contract_id=contract_id),
            headers=self.headers,
            timeout=4
        )

        if str(response.status_code).startswith(('4', '5')):
            return None

        return response.json()

    def get_current_pox_data(self) -> Dict[str, Any]:
        response = self._make_get_request(GET_CURRENT_POX_PATH, headers=self.headers, timeout=4)

        return response.json()

    def get_blocks(self, blocks_numbers: List[int]):
        """Get all blocks by the numbers"""
        blocks: List[Optional[StackBlock]] = []
        for block_detail_result in self._generate_blocks(blocks_numbers):
            if block_detail_result:
                blocks.append(self.block_mapper.json_dict_to_block(block_detail_result) if block_detail_result is not None else block_detail_result)
            
        return blocks

    def get_blocks_transactions(self, blocks_numbers: List[int], get_details: bool = True):
        """Get all block transactions by numbers"""
        _transactions: List[Dict[str, Any]] = []
        for block_transactions_result in self._generate_blocks_transactions(blocks_numbers):
                _transactions.extend(block_transactions_result)

        def get_invalid_transactions(transaction: Dict[str, Any]):
            events: Optional[List] = transaction.get('events')
            event_count: Optional[int] = transaction.get('event_count')
            return events is not None and event_count is not None and len(events) != event_count

        txs_hash = list(map(lambda tx: tx["tx_id"], filter(get_invalid_transactions, _transactions)))

        if get_details:
            transactions_mapping = self.get_details_transactions(txs_hash)

            transactions: List[StackTransaction] = list(
                map(lambda tx: self.transaction_mapper.json_dict_to_transaction(tx),
                    filter(
                        lambda tx: not get_invalid_transactions(tx), # get the valid transactions
                        _transactions
                    )
                )
            )

            for transaction in list(transactions_mapping.values()):
                transactions.append(self.transaction_mapper.json_dict_to_transaction(transaction["result"]))
        else:
            transactions = list(map(lambda tx: self.transaction_mapper.json_dict_to_transaction(tx), _transactions))

        return transactions

    def get_contracts_infos(self, contracts_ids: List[str]):
        contracts: List[StackContract] = []
        for contract_result in self._generate_get_contracts_info(contracts_ids):
            if contract_result:
                contracts.append(self.contract_mapper.json_dict_to_contract(contract_result))

        return contracts

    def _generate_blocks(self, blocks_numbers: List[int]):
        for block_number in blocks_numbers:
            yield self.get_block(block_number)

    def _generate_blocks_transactions(self, blocks_numbers: List[int]):
        for block_number in blocks_numbers:
            yield self.get_block_transactions(block_number)
    
    def _generate_get_contracts_info(self, contracts_ids: List[str]):
        for contract_id in contracts_ids:
            yield self.get_contract_info(contract_id)
