# Playground

Welcome to the MultiversX Development Playground.

## Test wallet

Create a test wallet on `Devnet`: https://devnet-wallet.multiversx.com. You can fund the newly created account directly from the Devnet Wallet (click on _Faucet_).

Then, place the test wallet (e.g. `wallet.json`) in the `sandbox` folder.

Alternatively, you can create a test wallet using `mxpy` (then fund it from the Devnet Wallet):

```
mxpy wallet new --format=keystore-mnemonic --outfile=$SANDBOX/wallet.json
```

## Sandbox

In the sandbox folder you can put files such as **test wallets**, **pre-built test contracts** and so on. 

Do not add any important files here.

## Smart Contracts

### Creating contracts

Create a contract using the `Adder` (contract) as a starting point (template):

```
mxpy contract new --template=adder --name=adder --path=$CONTRACTS
```

Create a contract using the `PingPong` (contract) as a starting point (template):

```
mxpy contract new --template=ping-pong-egld --name=ping-pong --path=$CONTRACTS
```

Upon creating a contract, make sure to reference it (and its `meta` crate) in `contracts/Cargo.toml`. For example:

```
[workspace]
resolver = "2"

members = [
    "adder",
    "adder/meta",
    "ping-pong",
    "ping-pong/meta"
]

```

### Building contracts

Build a contract that exists in the folder `adder` (relative path):

```
mxpy contract build --path=$CONTRACTS/adder

stat $CONTRACTS/adder/output/adder.wasm
```

Build a contract that exists in the folder `ping-pong-egld` (relative path):

```
mxpy contract build --path=$CONTRACTS/ping-pong

stat $CONTRACTS/ping-pong/output/ping-pong-egld.wasm
```

### Running tests

Run tests for `Adder`:

```
cd $CONTRACTS/adder

mxpy contract test
cargo test
```

Run tests for `PingPong`:

```
cd $CONTRACTS/ping-pong

mxpy contract test
cargo test
```

**Note:** some tests may fail due to incorrect paths - not completely handled when creating a new contract based on a template (as of November 2023). Make sure to manually fix the incorrect paths in the test files.

### Deploying contracts

The WASM bytecode files can be found in the `output` subirectory of each contract (upon a successful build).

Deploy `Adder`:

```
mxpy contract deploy --proxy=https://devnet-api.multiversx.com \
    --bytecode=$CONTRACTS/adder/output/adder.wasm --gas-limit=15000000 --arguments 0 \
    --keyfile=$SANDBOX/wallet.json --recall-nonce \
    --send
```

Deploy `PingPong`:

```
mxpy contract deploy --proxy=https://devnet-api.multiversx.com \
    --bytecode=$CONTRACTS/ping-pong/output/ping-pong-egld.wasm --gas-limit=25000000 --arguments 1000000000000000000 600 0x00 \
    --keyfile=$SANDBOX/wallet.json --recall-nonce \
    --send
```

Upon deployment, make sure to retain the addresses of the newly deploy contracts (displayed in `stdout`). Furthermore, inspect the deployment transactions and the contracts on Explorer.

## Snippets

### Python snippets

The folder `snippets-python` contains a few Python scripts (examples) that can be used to interact with the network and with some test contracts. Feel free to add more scripts, or to add more functionality to the existing ones.

```
python3 $SNIPPETS_PY/adder.py deploy --bytecode=$SANDBOX/adder.wasm
python3 $SNIPPETS_PY/adder.py add --contract=erd1qqqqqqqqqqqqqpgql5sllxejp8a9qzcn5qh6uvgqgk349p9ysv7sq26xhh --value=7
python3 $SNIPPETS_PY/adder.py get-sum --contract=erd1qqqqqqqqqqqqqpgql5sllxejp8a9qzcn5qh6uvgqgk349p9ysv7sq26xhh
```

### Javascript snippets

The folder `snippets-javascript` contains a few Javascript scripts (examples) that can be used to interact with the network and with some test contracts. Feel free to add more scripts, or to add more functionality to the existing ones.

```
node $SNIPPETS_JS/adder.js deploy --bytecode=$SANDBOX/adder.wasm
node $SNIPPETS_JS/adder.js add --contract=erd1qqqqqqqqqqqqqpgql5sllxejp8a9qzcn5qh6uvgqgk349p9ysv7sq26xhh --value=7
node $SNIPPETS_JS/adder.js get-sum --contract=erd1qqqqqqqqqqqqqpgql5sllxejp8a9qzcn5qh6uvgqgk349p9ysv7sq26xhh
```
