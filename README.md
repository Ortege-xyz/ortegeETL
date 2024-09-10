# Ortege ETL

[![Discord](https://img.shields.io/badge/discord-join%20chat-blue.svg)](https://discord.gg/ortege)

Ortege ETL lets you convert blockchain data into convenient formats like CSVs and stream the data into Kafka.

We've merged a few different codebases into a singular codebase to make it easier for developers to use one tool for all their data analytics needs. We'd like to thank all the great work done from these libraries which we've leveraged extensively:
[EthereumETL](https://github.com/blockchain-etl/ethereum-etl)
[BitcoinETL](https://github.com/blockchain-etl/bitcoin-etl)

# Create Wheel
`python setup.py bdist_wheel`

## Quickstart

Install Ortege ETL:

We will eventually setup OrtegeETL through PyPi but for now, please clone the repository locally and run it from the command line. 

Currently we support the following chains:
* EVM
* Bitcoin
* Stacks

### EVM
#### Export blocks and transactions 

```bash
ortegeetlevm export_blocks_and_transactions --start-block 0 --end-block 500000 \
--blocks-output blocks.csv --transactions-output transactions.csv \
--provider-uri https://mainnet.infura.io/v3/7aef3f0cd1f64408b163814b22cc643c
```

#### Export ERC20 and ERC721 transfers 

```bash
ortegeetl evm export_token_transfers --start-block 0 --end-block 500000 \
--provider-uri file://$HOME/Library/Ethereum/geth.ipc --output token_transfers.csv
```

#### Export traces 

```bash
ortegeetl evm export_traces --start-block 0 --end-block 500000 \
--provider-uri file://$HOME/Library/Ethereum/parity.ipc --output traces.csv
```

#### Stream blocks, transactions, logs, token_transfers continually to console 

```bash
ortegeetl evm stream --start-block 500000 -e block,transaction,log,token_transfer --log-file log.txt \
--provider-uri https://mainnet.infura.io/v3/7aef3f0cd1f64408b163814b22cc643c
```
### Bitcoin
#### Export blocks and transactions 

```bash
ortegeetl btc export_blocks_and_transactions --start-block 0 --end-block 500000 \
--provider-uri http://user:pass@localhost:8332 --chain bitcoin \
 --blocks-output blocks.json --transactions-output transactions.json
```

#### Stream blockchain data continually to console

```bash
ortegeetl btc stream -p http://user:pass@localhost:8332 --start-block 500000
```

### Stacks

### Soroban
**Coming soon**