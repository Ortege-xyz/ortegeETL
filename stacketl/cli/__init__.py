import click
from stacketl.cli.export_blocks_and_transactions import export_blocks_and_transactions

@click.group()
def stack():
    """All commands related with evm chains."""
    pass

stack.add_command(export_blocks_and_transactions)