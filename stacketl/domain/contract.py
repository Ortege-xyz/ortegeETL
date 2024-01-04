class StackContract(object):
    def __init__(self):
        self.tx_id = None
        self.canonical = None
        self.contract_id = None
        self.block_height = None
        self.clarity_version = None
        self.source_code = None
        self.abi = None
        self.is_erc20 = False
        self.is_erc721 = False