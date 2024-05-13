const readline = require("readline");
const fs = require("fs");
const path = require("path");
const { UserSigner } = require("@multiversx/sdk-wallet");
const { Address } = require("@multiversx/sdk-core");
const { HRP } = require("./constants");

async function pickSigner() {
    const entries = [];

    const folder = process.env.SANDBOX;
    const pemFiles = fs.readdirSync(folder).filter(file => path.extname(file) === ".pem");
    const jsonFiles = fs.readdirSync(folder).filter(file => path.extname(file) === ".json" && !file.endsWith(".abi.json"));

    for (const pemFile of pemFiles) {
        entries.push(path.join(folder, pemFile));
    }
    for (const jsonFile of jsonFiles) {
        entries.push(path.join(folder, jsonFile));
    }

    for (let i = 0; i < entries.length; i++) {
        console.log(`${i}: ${entries[i]}`);
    }

    const choice = parseInt(await askQuestion("Pick a signer: "));
    const filePath = entries[choice];
    const signer = await createSignerFromFile(filePath);
    const signerAddress = Address.fromBech32(signer.getAddress().bech32());

    return { signer, signerAddress };
}

async function createSignerFromFile(filePath) {
    const fileContent = fs.readFileSync(filePath, "utf8");

    if (filePath.endsWith(".pem")) {
        return UserSigner.fromPem(fileContent);
    } else if (filePath.endsWith(".json")) {
        const keyfileObject = JSON.parse(fileContent);
        const password = await askQuestion("Password: ", { hideEchoBack: true });
        return UserSigner.fromWallet(keyfileObject, password);
    } else {
        throw new Error("Unknown wallet type.");
    }
}

async function askQuestion(question, options) {
    const readlineInterface = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    const answer = await new Promise(resolve => {
        readlineInterface.question(question, resolve, options);
    });

    readlineInterface.close();

    return answer;
}

module.exports = {
    pickSigner
};
