# Smart Contracts

## Creating contracts

Create a contract using the `Adder` (contract) as a starting point (template):

```
mxpy contract new --template=adder adder
```

Create a contract using the `PingPong` (contract) as a starting point (template):

```
mxpy contract new --template=ping-pong-egld ping-pong-egld
```

## Building contracts

Build a contract that exists in the folder `adder` (relative path):

```
mxpy contract build --path=adder

stat adder/output/adder.wasm
```

Build a contract that exists in the folder `ping-pong-egld` (relative path):

```
mxpy contract build --path=ping-pong-egld

stat adder/output/ping-pong-egld.wasm
```

## Running contracts tests

Run tests for `Adder`:

```
cd adder

mxpy contract test
cargo test
```

Run tests for `PingPong`:

```
cd ping-pong-egld

mxpy contract test
cargo test
```
