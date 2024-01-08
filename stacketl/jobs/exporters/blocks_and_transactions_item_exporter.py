from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter

BLOCK_FIELDS_TO_EXPORT = [
    'hash',
    'number',
    'timestamp',
    'canonical'    
    'index_block_hash',
    'parent_block_hash',
    'burn_block_hash',
    'burn_block_height'
    'miner_txid',
    'parent_microblock_hash',
    'parent_microblock_sequence',
    'microblocks_accepted',
    'microblocks_streamed',
    'execution_cost_read_count',
    'execution_cost_read_length',
    'execution_cost_runtime',
    'execution_cost_write_count',
    'execution_cost_write_length',
    'microblock_tx_count',

]

TRANSACTION_FIELDS_TO_EXPORT = [
    'hash',
    'nonce',
    'sender_address',
    'tx_index',
    'tx_result',
    'fee_rate',
    'block_number',
    'block_hash',
    'block_timestamp',
    'event_count',
    'events',
    'tx_type',
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
