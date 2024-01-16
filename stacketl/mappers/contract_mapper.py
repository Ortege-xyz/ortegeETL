from stacketl.domain.contract import StackContract

class StackContractMapper(object):
    def json_dict_to_contract(self, json_dict):
        contract = StackContract()
        
        contract.tx_hash = json_dict['tx_id']
        contract.canonical = json_dict['canonical']
        contract.address = json_dict['contract_id']
        contract.block_number = json_dict['block_height']
        contract.clarity_version = json_dict['clarity_version']
        contract.source_code = json_dict['source_code']
        contract.abi = json_dict['abi']

        return contract

    def contract_to_dict(self, contract: StackContract):
        return {
            'type': 'contract',
            'address': contract.address,
            'tx_hash': contract.tx_hash,
            'canonical': contract.canonical,
            'source_code': contract.source_code,
            'abi': contract.abi,
            'is_stx20': contract.is_stx20,
            'is_nft': contract.is_nft,
            'block_number': contract.block_number,
            'clarity_version': contract.clarity_version,
        }
