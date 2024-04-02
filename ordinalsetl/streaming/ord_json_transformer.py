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
            'genesis_height': ins_json.get('genesis_height'),
            'genesis_fee': ins_json.get('genesis_fee'),
            'output_value': ins_json.get('output_value'),
            'content_type': ins_json.get('content_type'),
            'content_length': ins_json.get('content_length'),
            'timestamp': ins_json.get('timestamp'),
        }
