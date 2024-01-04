class StackBlock(object):
    def __init__(self):
        self.canonical = None
        self.height = None
        self.hash = None
        self.index_block_hash = None
        self.parent_block_hash = None
        self.burn_block_time = None
        self.burn_block_time_iso = None
        self.burn_block_hash = None
        self.burn_block_height = None
        self.miner_txid = None
        self.parent_microblock_hash = None
        self.parent_microblock_sequence = None
        self.txs = []
        self.microblocks_accepted = []
        self.microblocks_streamed = []
        self.execution_cost_read_count = None
        self.execution_cost_read_length = None
        self.execution_cost_runtime = None
        self.execution_cost_write_count = None
        self.execution_cost_write_length = None
        self.microblock_tx_count = None