# MIT License
#
# Copyright (c) 2018 Omidiora Samuel, samparsky@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from stacketl.domain.transaction import StackTransaction


# https://docs.hiro.so/api/get-block-by-height
# https://docs.hiro.so/api/get-transaction
class StackTransactionMapper(object):
    def json_dict_to_transaction(self, json_dict: dict, **kwargs):
        transaction = StackTransaction()
        transaction.hash = json_dict.get('tx_id')
        transaction.nonce = json_dict.get('nonce')
        transaction.fee_rate = json_dict.get('fee_rate')
        transaction.sender_address = json_dict.get('sender_address')
        transaction.sponsored = json_dict.get('sponsored')

        transaction.post_condition_mode = json_dict.get('post_condition_mode')
        transaction.post_conditions = json_dict.get('post_conditions')

        transaction.anchor_mode = json_dict.get('anchor_mode')
        transaction.is_unanchored = json_dict.get('is_unanchored')

        transaction.block_hash = json_dict.get('block_hash')
        transaction.block_timestamp = json_dict.get('burn_block_time')
        transaction.block_number = json_dict.get('block_height')
        transaction.parent_block_hash = json_dict.get('parent_block_hash')
        transaction.parent_burn_block_time = json_dict.get('parent_burn_block_time')

        transaction.canonical = json_dict.get('canonical')
        transaction.tx_index = json_dict.get('tx_index')
        transaction.tx_status = json_dict.get('tx_status')
        transaction.tx_result = json_dict.get('tx_result')

        transaction.microblock_hash = json_dict.get('microblock_hash')
        transaction.microblock_sequence = json_dict.get('microblock_sequence')
        transaction.microblock_canonical = json_dict.get('microblock_canonical')
    
        transaction.event_count = json_dict.get('event_count')
        transaction.events = json_dict.get('events')

        transaction.execution_cost_read_count = json_dict.get('execution_cost_read_count')
        transaction.execution_cost_read_length = json_dict.get('execution_cost_read_length')
        transaction.execution_cost_runtime = json_dict.get('execution_cost_runtime')
        transaction.execution_cost_write_count = json_dict.get('execution_cost_write_count')
        transaction.execution_cost_write_length = json_dict.get('execution_cost_write_length')

        transaction.tx_type = json_dict.get('tx_type')
        transaction.token_transfer = json_dict.get('token_transfer')
        transaction.coinbase_payload = json_dict.get('coinbase_payload')
        transaction.smart_contract = json_dict.get('smart_contract')
        transaction.contract_call = json_dict.get('contract_call')

        return transaction

    def transaction_to_dict(self, transaction: StackTransaction):
        return {
            'type': 'transaction',
            'hash': transaction.hash,
            'nonce': transaction.nonce,
            'fee_rate': transaction.fee_rate,
            'sender_address': transaction.sender_address,
            'sponsored': transaction.sponsored,
            'post_condition_mode': transaction.post_condition_mode,
            'post_conditions': transaction.post_conditions,
            'anchor_mode': transaction.anchor_mode,
            'is_unanchored': transaction.is_unanchored,
            'block_number': transaction.block_number,
            'block_hash': transaction.block_hash,
            'block_timestamp': transaction.timestamp,
            'parent_block_hash': transaction.parent_block_hash,
            'parent_burn_block_time': transaction.parent_burn_block_time,
            'canonical': transaction.canonical,
            'tx_index': transaction.tx_index,
            'tx_status': transaction.tx_status,
            'tx_result': transaction.tx_result,
            'microblock_hash': transaction.microblock_hash,
            'microblock_sequence': transaction.microblock_sequence,
            'microblock_canonical': transaction.microblock_canonical,
            'event_count': transaction.event_count,
            'events': transaction.events,
            'execution_cost_read_count': transaction.execution_cost_read_count,
            'execution_cost_read_length': transaction.execution_cost_read_length,
            'execution_cost_runtime': transaction.execution_cost_runtime,
            'execution_cost_write_count': transaction.execution_cost_write_count,
            'execution_cost_write_length': transaction.execution_cost_write_length,
            'tx_type': transaction.tx_type,
            'token_transfer': transaction.token_transfer,
            'coinbase_payload': transaction.coinbase_payload,
            'smart_contract': transaction.smart_contract,
            'contract_call': transaction.contract_call,
        }