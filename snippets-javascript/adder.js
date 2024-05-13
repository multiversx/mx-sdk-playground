const fs = require("fs");
const { Address, Transaction, SmartContract } = require("@multiversx/sdk-core");
const { applyChainID, broadcastTransaction, createSmartContractTransactionsFactory, queryContract, recallNonce, signTransaction } = require("./shared");
const { EXPLORER_URL } = require("./constants");
const { pickSigner } = require("./wallet");
const { Command } = require("commander");

const GAS_LIMIT_DEPLOY = 15000000;
const GAS_LIMIT_ADD = 5000000;
const ABI_FILE_PATH = `${process.env.SANDBOX}/adder.abi.json`;

(async () => {
    await main();
})();

async function main() {
    const program = new Command();

    program
        .command("deploy")
        .requiredOption("--bytecode <path>", "Path to the bytecode")
        .action(deploy);

    program
        .command("add")
        .requiredOption("--contract <address>", "Contract address")
        .requiredOption("--value <value>", "Value")
        .action(add);

    program
        .command("get-sum")
        .requiredOption("--contract <address>", "Contract address")
        .action(getSum);

    program.parse(process.argv);
}

async function deploy(args) {
    const bytecodePath = args.bytecode;
    const { signer, signerAddress } = await pickSigner();
    const factory = createSmartContractTransactionsFactory(ABI_FILE_PATH);

    const bytecode = fs.readFileSync(bytecodePath);

    const draftTransaction = factory.createTransactionForDeploy({
        sender: signerAddress,
        bytecode: bytecode,
        gasLimit: GAS_LIMIT_DEPLOY,
        args: [0]
    });

    const transaction = Transaction.fromDraft(draftTransaction);

    applyChainID(transaction);
    await recallNonce(transaction);
    await signTransaction(transaction, signer);
    await broadcastTransaction(transaction);

    const contractAddress = SmartContract.computeAddress(signerAddress, transaction.nonce);

    console.log("Contract address:");
    console.log(`${EXPLORER_URL}/accounts/${contractAddress.bech32()}`);
}

async function add(args) {
    const contractAddress = Address.fromBech32(args.contract);
    const value = args.value;

    const { signer, signerAddress } = await pickSigner();
    const factory = createSmartContractTransactionsFactory(ABI_FILE_PATH);

    const draftTransaction = factory.createTransactionForExecute({
        sender: signerAddress,
        contract: contractAddress,
        functionName: "add",
        gasLimit: GAS_LIMIT_ADD,
        args: [value]
    });

    const transaction = Transaction.fromDraft(draftTransaction);

    applyChainID(transaction);
    await recallNonce(transaction);
    await signTransaction(transaction, signer);
    await broadcastTransaction(transaction);
}

async function getSum(args) {
}

