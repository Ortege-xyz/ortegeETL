from typing import List
from stacketl.domain.transaction import StackTransaction

class StackBlock(object):
    def __init__(self):
        self.canonical = None
        self.number = None
        self.hash = None
        self.timestamp = None
        self.index_block_hash = None
        self.parent_block_hash = None
        self.burn_block_hash = None
        self.burn_block_height = None
        self.miner_txid = None
        self.execution_cost_read_count = None
        self.execution_cost_read_length = None
        self.execution_cost_runtime = None
        self.execution_cost_write_count = None
        self.execution_cost_write_length = None

        self.transactions: List[StackTransaction] = []
        self.transaction_count = 0
        