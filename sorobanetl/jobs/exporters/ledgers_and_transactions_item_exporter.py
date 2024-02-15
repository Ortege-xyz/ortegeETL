from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter

LEDGER_FIELDS_TO_EXPORT = [
    'hash',
    'sequence',
    'timestamp',
    'prev_hash'    
    'closed_at',
    'total_coins',
    'fee_pool',
    'base_fee_in_stroops',
    'base_reserve_in_stroops',
    'max_tx_set_size',
    'protocol_version',
    'header_xdr',
    'successful_transaction_count',
    'failed_transaction_count',
    'operation_count',
]

TRANSACTION_FIELDS_TO_EXPORT = [
    'hash',
    'ledger',
    'datetime',
    'created_at',
    'source_account',
    'source_account_sequence',
    'fee_account',
    'fee_charged',
    'max_fee',
    'operation_count',
    'envelope_xdr',
    'result_xdr',
    'signatures',
    'preconditions'
]


def ledgers_and_transactions_item_exporter(ledgers_output=None, transactions_output=None):
    filename_mapping = {}
    field_mapping = {}

    if ledgers_output is not None:
        filename_mapping['ledger'] = ledgers_output
        field_mapping['ledger'] = LEDGER_FIELDS_TO_EXPORT

    if transactions_output is not None:
        filename_mapping['transaction'] = transactions_output
        field_mapping['transaction'] = TRANSACTION_FIELDS_TO_EXPORT

    return CompositeItemExporter(
        filename_mapping=filename_mapping,
        field_mapping=field_mapping
    )
