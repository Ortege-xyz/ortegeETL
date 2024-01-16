import json
import logging


class StackItemIdCalculator:

    def calculate(self, item):
        if item is None or not isinstance(item, dict):
            return None

        item_type = item.get('type')

        if item_type in ('block', 'transaction') and item.get('hash') is not None:
            return concat(item_type, item.get('hash'))
        
        if item_type == 'contract':
            return concat(item_type, item.get('address'))

        logging.warning('item_id for item {} is None'.format(json.dumps(item)))

        return None


def concat(*elements):
    return '_'.join([str(elem) for elem in elements])
