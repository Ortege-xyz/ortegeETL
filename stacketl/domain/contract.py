class StackContract(object):
    def __init__(self):
        self.tx_hash = None
        self.canonical = None
        self.contract_id = None
        self.block_number = None
        self.clarity_version = None
        self.source_code = None
        self.abi = None
        self.is_stx20 = False
        self.is_nft = False