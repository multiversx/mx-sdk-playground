const fs = require("fs");
const { ApiNetworkProvider } = require("@multiversx/sdk-network-providers");
const { SmartContractTransactionsFactory } = require("@multiversx/sdk-core/out/transactionsFactories");
const { TransactionsFactoryConfig } = require("@multiversx/sdk-core/out/transactionsFactories");
const { TokenComputer } = require("@multiversx/sdk-core");
const { AbiRegistry } = require("@multiversx/sdk-core");
const { API_URL, CHAIN_ID, EXPLORER_URL } = require("./constants");

function applyChainID(transaction) {
    transaction.setChainID(CHAIN_ID);
}

async function recallNonce(transaction) {
    const networkProvider = createNetworkProvider();
    const sender = transaction.sender;
    const account = await networkProvider.getAccount(sender);
    transaction.nonce = account.nonce;
}

async function signTransaction(transaction, signer) {
    const bytesForSigning = transaction.serializeForSigning();
    transaction.signature = await signer.sign(bytesForSigning);
}

async function broadcastTransaction(transaction) {
    const networkProvider = createNetworkProvider();
    const hash = await networkProvider.sendTransaction(transaction);

    console.log("See transaction:");
    console.log(`${EXPLORER_URL}/transactions/${hash}`);
}

function queryContract(address, func, arguments) {
}

function createSmartContractTransactionsFactory(abiFilePath) {
    const abiFileContent = fs.readFileSync(abiFilePath, { encoding: "utf8" });
    const abiObject = JSON.parse(abiFileContent);
    const abiRegistry = AbiRegistry.create(abiObject);

    const factoryConfig = new TransactionsFactoryConfig(CHAIN_ID);
    const factory = new SmartContractTransactionsFactory({
        config: factoryConfig,
        abi: abiRegistry,
        tokenComputer: new TokenComputer()
    });

    return factory;
}

function createNetworkProvider() {
    return new ApiNetworkProvider(API_URL);
}

module.exports = {
    applyChainID,
    recallNonce,
    signTransaction,
    broadcastTransaction,
    queryContract,
    createSmartContractTransactionsFactory
};
