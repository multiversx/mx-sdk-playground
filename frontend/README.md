# Frontend

## Creating dApps

Create a frontend for the contract `Adder` using `mx-template-dapp` as a starting point:

```
git clone --depth=1 --branch=main https://github.com/multiversx/mx-template-dapp.git adder && rm -rf ./adder/.git && rm -rf ./adder/.github
```

Create frontend for the contract `PingPong` using `mx-template-dapp` as a starting point:

```
git clone --depth=1 --branch=main https://github.com/multiversx/mx-template-dapp.git ping-pong && rm -rf ./ping-pong/.git && rm -rf ./ping-pong/.github
```

## Building the dApps

```
cd adder

yarn install
```


## Starting the dApps

```
cd adder

yarn start:devnet
```
