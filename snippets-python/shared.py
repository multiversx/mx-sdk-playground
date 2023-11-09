from typing import Any, Sequence
from multiversx_sdk_core import Address, ContractQueryBuilder, Transaction, TransactionComputer
from multiversx_sdk_network_providers import ApiNetworkProvider
from multiversx_sdk_wallet import UserSigner

from multiversx_sdk_core.transaction_factories import TransactionsFactoryConfig, SmartContractTransactionsFactory
from multiversx_sdk_core import TokenComputer, Address

from constants import API_URL, CHAIN_ID, EXPLORER_URL


def recall_nonce(transaction: Transaction):
    network_provider = create_network_provider()
    sender = Address.new_from_bech32(transaction.sender)
    account = network_provider.get_account(sender)
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


def query_contract(address: Address, function: str, arguments: Sequence[Any]) -> Any:
    query = ContractQueryBuilder(
        contract=address,
        function=function,
        call_arguments=arguments
    ).build()

    network_provider = create_network_provider()
    response = network_provider.query_contract(query)
    return response


def create_smart_contract_transactions_factory():
    factory_config = TransactionsFactoryConfig(CHAIN_ID)
    factory = SmartContractTransactionsFactory(factory_config, TokenComputer())
    return factory


def create_network_provider():
    return ApiNetworkProvider(API_URL)
