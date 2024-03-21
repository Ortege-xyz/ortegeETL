import json
import logging


class SorobanItemIdCalculator:

    def calculate(self, item):
        if item is None or not isinstance(item, dict):
            return None

        item_type = item.get('type')
        
        if item_type == 'ledger':
            return concat(item_type, item.get('sequence'))
        
        if item_type == 'transaction':
            return concat(item_type, item.get('hash'))
        
        if item_type == 'event':
            return concat(item_type, item.get('id'))

        logging.warning('item_id for item {} is None'.format(json.dumps(item)))

        return None


def concat(*elements):
    return '_'.join([str(elem) for elem in elements])
