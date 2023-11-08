
import base64
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, List

from multiversx_sdk_core.transaction_factories import TransactionsFactoryConfig, SmartContractTransactionsFactory
from multiversx_sdk_core import AddressComputer, ContractQueryBuilder, TokenComputer, Address, Transaction, TransactionComputer
from multiversx_sdk_wallet import UserSigner
from multiversx_sdk_core.codec import decode_unsigned_number
from constants import API_URL, CHAIN_ID, EXPLORER_URL
from wallet import pick_a_signer
from multiversx_sdk_network_providers import ApiNetworkProvider


GAS_LIMIT_DEPLOY = 15000000
GAS_LIMIT_ADD = 5000000


def main(cli_args: List[str]):
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser("deploy")
    subparser.add_argument("--bytecode", type=Path, required=True)
    subparser.set_defaults(func=deploy)

    subparser = subparsers.add_parser("add")
    subparser.add_argument("--contract", type=str, required=True)
    subparser.add_argument("--value", type=int, required=True)
    subparser.set_defaults(func=add)

    subparser = subparsers.add_parser("get-sum")
    subparser.add_argument("--contract", type=str, required=True)
    subparser.set_defaults(func=get_sum)

    args = parser.parse_args(cli_args)

    if not hasattr(args, "func"):
        parser.print_help()
    else:
        args.func(args)


def deploy(args: Any):
    bytecode_path = args.bytecode
    signer, signer_address = pick_a_signer()
    factory = create_transactions_factory()

    transaction = factory.create_transaction_for_deploy(
        sender=signer_address,
        bytecode=bytecode_path,
        gas_limit=GAS_LIMIT_DEPLOY,
        arguments=[0]
    )

    recall_nonce(transaction)
    sign_transaction(transaction, signer)
    broadcast_transaction(transaction)

    address_computer = AddressComputer()
    contract_address = address_computer.compute_contract_address(signer_address, transaction.nonce)

    print("Contract address:")
    print(f"{EXPLORER_URL}/accounts/{contract_address.to_bech32()}")


def add(args: Any):
    contract_address = Address.new_from_bech32(args.contract)
    value = args.value

    signer, signer_address = pick_a_signer()
    factory = create_transactions_factory()

    transaction = factory.create_transaction_for_execute(
        sender=signer_address,
        contract=contract_address,
        function="add",
        gas_limit=GAS_LIMIT_ADD,
        arguments=[value]
    )

    recall_nonce(transaction)
    sign_transaction(transaction, signer)
    broadcast_transaction(transaction)


def get_sum(args: Any):
    contract_address = Address.new_from_bech32(args.contract)

    query = ContractQueryBuilder(
        contract=contract_address,
        function="getSum",
        call_arguments=[]
    ).build()

    network_provider = create_network_provider()
    response = network_provider.query_contract(query)
    [value_base64, ] = response.return_data
    value_bytes = base64.b64decode(value_base64)
    value = decode_unsigned_number(value_bytes)

    print("Return code:", response.return_code)
    print("Return data:", response.return_data)
    print("Sum:", value)


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


def create_transactions_factory():
    factory_config = TransactionsFactoryConfig(CHAIN_ID)
    factory = SmartContractTransactionsFactory(factory_config, TokenComputer())
    return factory


def create_network_provider():
    return ApiNetworkProvider(API_URL)


if __name__ == "__main__":
    main(sys.argv[1:])
