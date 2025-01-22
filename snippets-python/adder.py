
import base64
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, List

from multiversx_sdk import AddressComputer, Address
from shared import broadcast_transaction, create_smart_contract_transactions_factory, query_contract, recall_nonce, sign_transaction
from constants import EXPLORER_URL
from wallet import pick_a_signer


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
    factory = create_smart_contract_transactions_factory()

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
    factory = create_smart_contract_transactions_factory()

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

    response = query_contract(
        address=contract_address,
        function="getSum",
        arguments=[]
    )

    [value_bytes] = response.return_data_parts
    value = int.from_bytes(bytes=value_bytes, byteorder="big", signed=False)

    print("Return code:", response.return_code)
    print("Return message:", response.return_message)
    print("Sum:", value)


if __name__ == "__main__":
    main(sys.argv[1:])
