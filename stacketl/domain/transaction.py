class StackTransaction(object):
    def __init__(self):
        self.hash = None
        self.nonce = None
        self.fee_rate = None
        self.sender_address = None
        self.sponsored = None

        self.post_condition_mode = None
        self.post_conditions = None

        self.anchor_mode = None
        self.is_unanchored = None

        self.block_number = None
        self.block_hash = None
        self.block_timestamp = None
        self.parent_block_hash = None
        self.parent_burn_block_time = None

        self.canonical = None
        self.tx_index = None
        self.tx_status = None
        self.tx_result = {}

        self.microblock_hash = None
        self.microblock_sequence = None
        self.microblock_canonical

        self.event_count = None
        self.events = []

        self.execution_cost_read_count = None
        self.execution_cost_read_length = None
        self.execution_cost_runtime = None
        self.execution_cost_write_count = None
        self.execution_cost_write_length = None

        self.tx_type = None
        self.token_transfer = None
        self.coinbase_payload = None
        self.smart_contract = None
        self.contract_call = None