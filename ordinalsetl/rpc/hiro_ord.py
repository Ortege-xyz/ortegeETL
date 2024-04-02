from blockchainetl.api_requester import ApiRequester
from ordinalsetl.rpc.ord_rpc import OrdRpc
from typing import Optional

GET_STATUS = "ordinals/v1/"
GET_INSCRIPTION_ID = "ordinals/v1/inscriptions/{id}"
GET_INSCRIPTION_TRANSFER = "ordinals/v1/inscriptions/transfers"

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
            return data
        return None

    def get_inscriptions_by_block(self, block_number: int):
        response = self._make_get_request(
            GET_INSCRIPTION_TRANSFER,
            params={'block': block_number},
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
