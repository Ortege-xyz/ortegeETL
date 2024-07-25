from blockchainetl.api_requester import ApiRequester
from ordinalsetl.rpc.ord_rpc import OrdRpc
from typing import List, Optional

GET_STATUS = "ordinals/v1/"
GET_INSCRIPTION_ID = "ordinals/v1/inscriptions/{id}"
GET_INSCRIPTIONS = "ordinals/v1/inscriptions"

INSCRIPTIONS_LIMIT = 60

class HiroOrdAPI(OrdRpc, ApiRequester):

    def __init__(self, api_url: str, api_key: Optional[str] = None, timeout=10):
        self.timeout = timeout
        if api_key:
            rate_limit = 490/60
        else:
            rate_limit = 45/60

        ApiRequester.__init__(self, api_url, api_key, rate_limit)
        
        self.headers = {'Accept': 'application/json'}
        if self.api_key:
            self.headers['x-hiro-api-key'] = self.api_key

    def get_block_height(self):
        response = self._make_get_request(GET_STATUS, headers=self.headers, timeout=self.timeout)
        if response.ok:
            data = response.json()
            return data["block_height"]
        return None

    def get_inscription_by_id(self, inscription_id):
        response = self._make_get_request(
            GET_INSCRIPTION_ID.format(id=inscription_id),
            headers=self.headers,
            timeout=self.timeout
        )
        if response.ok:
            data = response.json()
            data['inscription_id'] = data.pop('id')
            data['genesis_height'] = data.pop('genesis_block_height')
            data['genesis_hash'] = data.pop('genesis_block_hash')
            data['output_value'] = data.pop('value')
            return data
        return None

    def get_inscriptions_by_block(self, block_number: int):
        response = self._make_get_request(
            GET_INSCRIPTIONS,
            params={'genesis_block': block_number, 'limit': 60},
            headers=self.headers,
            timeout=self.timeout
        )
        if response.ok :
            data = response.json()
            data['inscriptions'] = []
            for ins in data['results']:
                data['inscriptions'].append(ins['id'])
            return data
        return None
    
    def get_inscriptions_by_blocks(self, from_block: int, to_block: int):
        inscriptions: List[dict] = []
        offset = 0
        while True:
            response = self._make_get_request(
                GET_INSCRIPTIONS,
                params={
                    'from_genesis_block_height': from_block, 
                    'to_genesis_block_height': to_block, 
                    'limit': INSCRIPTIONS_LIMIT,
                    'offset:': offset,
                },
                headers=self.headers,
                timeout=self.timeout
            )
            if response.ok :
                data = response.json()
                inscriptions.extend(data['results'])

                if len(inscriptions) < data['total']:
                    offset += INSCRIPTIONS_LIMIT
                else:
                    break
        return inscriptions
