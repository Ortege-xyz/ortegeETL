import requests
from typing import Any, Optional

from stacketl.mappers.block_mapper import StackBlockMapper

GET_BLOCK = '/extended/v1/block/by_height/{number}'
GET_TRANSACTION = '/extended/v1/tx/{hash}'

class StackApi():
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.block_mapper = StackBlockMapper()

    def get_block(self, block_number: int) -> Optional[dict[str, Any]]:
        url = self.api_url + GET_BLOCK
        try:
            response = requests.get(url.format(number=block_number))

            if str(response.status_code).startswith(('4', '5')):
                return None
            
            return response.json()
        except:
            return None

    def get_blocks(self, blocks_numbers: list[int]):
        blocks_result = list(self._generate_blocks(blocks_numbers))
        blocks = [self.block_mapper.json_dict_to_block(block_detail_result)
                  for block_detail_result in blocks_result]
        return blocks

    def _generate_blocks(self, blocks_numbers: list[int]):
        for block_number in blocks_numbers:
            yield self.get_block(block_number)
            