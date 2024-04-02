import decimal
import json
import requests


class OrdRpc:

    def __init__(self, provider_uri, timeout=60):
        self.provider_uri = provider_uri
        self.timeout = timeout

    def get_block_height(self):
        url = self.provider_uri + '/blockheight'
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers, timeout=self.timeout)
        return response.json() if response.ok else None

    def get_inscription_by_id(self, inscription_id):
        url = "{}/inscription/{}".format(self.provider_uri, inscription_id)
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers, timeout=self.timeout)
        return response.json() if response.ok else None

    def get_inscriptions_by_block(self, block_number):
        url = "{}/inscriptions/block/{}".format(self.provider_uri, block_number)
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers, timeout=self.timeout)
        return response.json() if response.ok else None
