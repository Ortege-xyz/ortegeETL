from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter

CONTRACTS_FIELDS_TO_EXPORT = [
    'address',
    'block_number',
    'tx_hash',
    'canonical',
    'is_stx20',
    'is_nft',
]


def contracts_item_exporter(contracts_output=None):
    filename_mapping = {}
    field_mapping = {}

    if contracts_output is not None:
        filename_mapping['contract'] = contracts_output
        field_mapping['contract'] = CONTRACTS_FIELDS_TO_EXPORT

    return CompositeItemExporter(
        filename_mapping=filename_mapping,
        field_mapping=field_mapping
    )
