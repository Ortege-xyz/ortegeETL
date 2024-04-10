import json
import logging


class AptosItemIdCalculator:

    def calculate(self, item):
        if item is None or not isinstance(item, dict):
            return None

        item_type = item.get('type')
        
        if item_type == 'block':
            return concat(item_type, item.get('number'))
        
        if item_type == 'transaction':
            return concat(item_type, item.get('hash'))

        logging.warning('item_id for item {} is None'.format(json.dumps(item)))

        return None


def concat(*elements):
    return '_'.join([str(elem) for elem in elements])
