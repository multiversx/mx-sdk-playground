from typing import Any

from multiversx_sdk import (
    Address,
    ApiNetworkProvider,
    SmartContractController,
    SmartContractQueryResponse,
    SmartContractTransactionsFactory,
    Transaction,
    TransactionComputer,
    TransactionsFactoryConfig,
    UserSigner
)

from constants import API_URL, CHAIN_ID, EXPLORER_URL


def recall_nonce(transaction: Transaction):
    network_provider = create_network_provider()
    account = network_provider.get_account(transaction.sender)
    transaction.nonce = account.nonce


def sign_transaction(transaction: Transaction, signer: UserSigner):
    computer = TransactionComputer()
    bytes_for_signing = computer.compute_bytes_for_signing(transaction)
    transaction.signature = signer.sign(bytes_for_signing)


def broadcast_transaction(transaction: Transaction):
    network_provider = create_network_provider()
    hash = network_provider.send_transaction(transaction)

    print("See transaction:")
    print(f"{EXPLORER_URL}/transactions/{hash}")


def query_contract(address: Address, function: str, arguments: list[Any]) -> SmartContractQueryResponse:
    sc_controller = SmartContractController(chain_id=CHAIN_ID, network_provider=create_network_provider())
    query = sc_controller.create_query(
        contract=address,
        function=function,
        arguments=arguments
    )

    response = sc_controller.run_query(query)
    return response


def create_smart_contract_transactions_factory():
    factory_config = TransactionsFactoryConfig(CHAIN_ID)
    factory = SmartContractTransactionsFactory(factory_config)
    return factory


def create_network_provider():
    return ApiNetworkProvider(API_URL)
