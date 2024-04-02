class OrdJsonTransformer(object):
    def __init__(self):
        pass

    def format_inscription(self, ins_json):
        return {
            # Message fields for Pub/Sub exporter
            'type': 'inscription',
            'item_id': 'inscription_' + ins_json.get('inscription_id'),
            # Regular fields
            'inscription_id': ins_json.get('inscription_id'),
            'inscription_number': ins_json.get('number'),
            'address': ins_json.get('address'),
            'genesis_address': ins_json.get('genesis_address'),
            'genesis_height': ins_json.get('genesis_height'),
            'genesis_hash': ins_json.get('genesis_hash'),
            'genesis_tx_id': ins_json.get('genesis_tx_id'),
            'genesis_fee': ins_json.get('genesis_fee'),
            'value': ins_json.get('output_value'),
            'output': ins_json.get('output'),
            'offset': ins_json.get('offset'),
            'location': ins_json.get('location'),
            'content_type': ins_json.get('content_type'),
            'content_length': ins_json.get('content_length'),
            'timestamp': ins_json.get('timestamp'),
            'sat_ordinal': ins_json.get('sat_ordinal'),
            'sat_rarity': ins_json.get('sat_rarity'),
            'sat_coinbase_height': ins_json.get('sat_coinbase_height'),
        }
