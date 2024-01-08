from typing import Optional

from stacketl.domain.block import StackBlock
from stacketl.mappers.transaction_mapper import StackTransactionMapper


class StackBlockMapper(object):
    def __init__(self, transaction_mapper: Optional[StackTransactionMapper] = None):
        if transaction_mapper is None:
            self.transaction_mapper = StackTransactionMapper()
        else:
            self.transaction_mapper = transaction_mapper

    def json_dict_to_block(self, json_dict: dict):
        block = StackBlock()
        block.canonical = json_dict.get('canonical')
        block.number = json_dict.get('height')
        block.hash = json_dict.get('hash')
        block.timestamp = json_dict.get('burn_block_time')
        block.index_block_hash = json_dict.get('index_block_hash')
        block.parent_block_hash = json_dict.get('parent_block_hash')
        block.burn_block_hash = json_dict.get('burn_block_hash')
        block.burn_block_height = json_dict.get('burn_block_height')
        block.miner_txid = json_dict.get('miner_txid')
        block.parent_microblock_hash = json_dict.get('parent_microblock_hash')
        block.parent_microblock_sequence = json_dict.get('parent_microblock_sequence')
        block.execution_cost_read_count = json_dict.get('execution_cost_read_count')
        block.execution_cost_read_length = json_dict.get('execution_cost_read_length')
        block.execution_cost_runtime = json_dict.get('execution_cost_runtime')
        block.execution_cost_write_count = json_dict.get('execution_cost_write_count')
        block.execution_cost_write_length = json_dict.get('execution_cost_write_length')
        block.microblock_tx_count = json_dict.get('microblock_tx_count')

        block.transactions = json_dict.get('txs')
        block.transaction_count = len(block.transactions)

        return block

    def block_to_dict(self, block: StackBlock):
        return {
            'type': 'block',
            'canonical': block.canonical,
            'number': block.number,
            'hash': block.hash,
            'timestamp': block.timestamp,
            'index_block_hash': block.index_block_hash,
            'parent_block_hash': block.parent_block_hash,
            'burn_block_hash': block.burn_block_hash,
            'burn_block_height': block.burn_block_height,
            'miner_txid': block.miner_txid,
            'parent_microblock_hash': block.parent_microblock_hash,
            'parent_microblock_sequence': block.parent_microblock_sequence,
            'execution_cost_read_count': block.execution_cost_read_count,
            'execution_cost_read_length': block.execution_cost_read_length, 
            'execution_cost_runtime': block.execution_cost_runtime,
            'execution_cost_write_count': block.execution_cost_write_count,
            'execution_cost_write_length': block.execution_cost_write_length, 
            'microblock_tx_count': block.microblock_tx_count,
        }

