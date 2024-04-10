from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter

BLOCK_FIELDS_TO_EXPORT = [
    'number',
    'hash',
    'timestamp',
    'first_version',
    'last_version',
]

TRANSACTION_FIELDS_TO_EXPORT = [
    'hash',
    'block_number',
    'state_change_hash',
    'event_root_hash',
    'version',
    'gas_used',
    'success',
    'vm_status',
    'accumulator_root_hash',
    'changes',
    'tx_type',
    'sender',
    'state_checkpoint_hash',
    'id',
    'epoch',
    'round',
    'previous_block_votes_bitvec',
    'proposer',
    'failed_proposer_indices',
    'timestamp',
    'max_gas_amount',
    'gas_unit_price',
    'expiration_timestamp_secs',
    'payload',
    'events',
    'signature',
]

def blocks_and_transactions_item_exporter(blocks_output=None, transactions_output=None):
    filename_mapping = {}
    field_mapping = {}

    if blocks_output is not None:
        filename_mapping['block'] = blocks_output
        field_mapping['block'] = BLOCK_FIELDS_TO_EXPORT

    if transactions_output is not None:
        filename_mapping['transaction'] = transactions_output
        field_mapping['transaction'] = TRANSACTION_FIELDS_TO_EXPORT

    return CompositeItemExporter(
        filename_mapping=filename_mapping,
        field_mapping=field_mapping
    )
