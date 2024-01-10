import click
from stacketl.cli.export_blocks_and_transactions import export_blocks_and_transactions
from stacketl.cli.export_contracts import export_contracts

@click.group()
def stacks():
    """All commands related with stack-like chains."""
    pass

stacks.add_command(export_blocks_and_transactions, "export_blocks_and_transactions")
stacks.add_command(export_contracts, "export_contracts")