from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter

EVENTS_FIELDS_TO_EXPORT = [
    'event_type',
    'ledger',
    'ledger_closed_at',
    'contract_id',
    'tx_hash',
    'id',
    'paging_token',
    'topic',
    'value',
    'in_successful_contract_call',
]


def events_item_exporter(events_output=None):
    filename_mapping = {}
    field_mapping = {}

    if events_output is not None:
        filename_mapping['event'] = events_output
        field_mapping['event'] = EVENTS_FIELDS_TO_EXPORT

    return CompositeItemExporter(
        filename_mapping=filename_mapping,
        field_mapping=field_mapping
    )
