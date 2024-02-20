# Playground

Welcome to the MultiversX Development Playground.

## Test wallet

Create a test wallet on `Devnet`: https://devnet-wallet.multiversx.com. You can fund the newly created account directly from the Devnet Wallet (click on _Faucet_).

Then, place the test wallet (e.g. `wallet.pem`) in the `sandbox` folder.

Alternatively, you can create a test wallet using `mxpy` (then fund it from the Devnet Wallet):

```
mxpy wallet new --format=pem --outfile=$SANDBOX/wallet.pem
```

## Sandbox

In the sandbox folder you can put files such as **test wallets**, **pre-built test contracts** and so on.

Do not add any important files here.

## Smart Contracts

### Creating contracts

Create a contract using the `Adder` (contract) as a starting point (template):

```
sc-meta new --template=adder --name=adder --path=$CONTRACTS
```

Create a contract using the `PingPong` (contract) as a starting point (template):

```
sc-meta new --template=ping-pong-egld --name=ping-pong --path=$CONTRACTS
```

Upon creating a contract, make sure to reference it in `.vscode/settings.json`, so that `rust-analyzer` is able to discover it:

```
"rust-analyzer.linkedProjects": [
    "contracts/adder/Cargo.toml",
    "contracts/ping-pong/Cargo.toml"
]
```

### Building contracts

Build a contract that exists in the folder `adder` (relative path):

```
sc-meta all build --path=$CONTRACTS/adder

stat $CONTRACTS/adder/output/adder.wasm
```

Build a contract that exists in the folder `ping-pong` (relative path):

```
sc-meta all build --path=$CONTRACTS/ping-pong

stat $CONTRACTS/ping-pong/output/ping-pong.wasm
```

### Running tests

Run tests for `Adder`:

```
sc-meta test --path=$CONTRACTS/adder
```

Run tests for `PingPong`:

```
sc-meta test --path=$CONTRACTS/ping-pong
```

### Deploying contracts

The WASM bytecode files can be found in the `output` subirectory of each contract (upon a successful build).

Deploy `Adder`:

```
mxpy contract deploy --proxy=https://devnet-api.multiversx.com \
    --bytecode=$CONTRACTS/adder/output/adder.wasm --gas-limit=15000000 --arguments 0 \
    --pem=$SANDBOX/wallet.pem --recall-nonce \
    --send
```

Deploy `PingPong`:

```
mxpy contract deploy --proxy=https://devnet-api.multiversx.com \
    --bytecode=$CONTRACTS/ping-pong/output/ping-pong.wasm --gas-limit=25000000 --arguments 1000000000000000000 600 0x00 \
    --pem=$SANDBOX/wallet.pem --recall-nonce \
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
