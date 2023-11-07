# Frontend

Documentation:
 - [`sdk-dapp`](https://docs.multiversx.com/sdk-and-tools/sdk-dapp)
 - [Your first dApp](https://docs.multiversx.com/developers/tutorials/your-first-dapp)

## Creating dApps

Create a frontend for the contract(s) using `mx-template-dapp` as a starting point (example):

```
new_dapp.sh adder
new_dapp.sh ping-pong
```

## Building the dApps

Install dependencies using `yarn` (example):

```
cd $FRONTEND/adder && yarn install
cd $FRONTEND/ping-pong && yarn install
```

## Starting the dApps

Start a dApps by invoking the `start:devnet` script (example):

```
cd $FRONTEND/adder && yarn start:devnet
cd $FRONTEND/ping-pong && yarn start:devnet
```
