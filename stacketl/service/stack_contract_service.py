STX20_FUNCTIONS = ["get-total-supply", "get-symbol", "get-name", "get-decimals", "get-balance", "get-token-uri", "transfer"]
NFT_FUNCTIONS = ["get-last-token-id", "get-token-uri", "get-owner", "transfer"]

class StackContractService:
    # https://docs.stacks.co/docs/cookbook/creating-an-ft
    def is_stx20_contract(self, functions):
        return all((stx20_function in functions) for stx20_function in STX20_FUNCTIONS)

    # https://docs.stacks.co/docs/cookbook/creating-an-nft
    def is_nft_contract(self, functions):
        return all((nft_function in functions) for nft_function in NFT_FUNCTIONS)
