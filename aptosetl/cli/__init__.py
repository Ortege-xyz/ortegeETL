import click
from aptosetl.cli.export_blocks_and_transactions import export_blocks_and_transactions


@click.group()
def aptos():
    """All commands related with aptos-like chains."""
    pass

aptos.add_command(export_blocks_and_transactions, "export_blocks_and_transactions")