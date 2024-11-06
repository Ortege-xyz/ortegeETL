# 2.0.3
StacksETL when streaming data is missing data under `events` for `event_type = fungible_token_asset`. The asset_id is missing in a lot of records.

Changes
* Added `get_transaction` function to StackAPI Class

# 2.0.2
Bitcoin RPC doesn't accept authentication within the URL. Since we've moved away from QuickNodes to hosting our own Bitcoin Nodes we need to include RPC username and password authentication. This change adjusts the bitcoin `request.py` in order to correctly handle credentials.

# 2.0.1
Adding logging for Stacks Streamer Adaptor to debug issue where transactions and contracts aren't producing

# 2.0.0
**Breaking Change** - Removed reliance on setting up last synced block from a file 