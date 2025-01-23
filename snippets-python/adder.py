import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from multiversx_sdk import Account, AddressComputer, Address, DevnetEntrypoint
from multiversx_sdk.abi import Abi
from constants import EXPLORER_URL
from wallet import pick_a_signer


GAS_LIMIT_DEPLOY = 15000000
GAS_LIMIT_ADD = 5000000

sandbox = Path(__file__).parent.parent / "sandbox"


def main(cli_args: list[str]):
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
    signer = pick_a_signer()
    account = Account(signer.secret_key)

    entrypoint = DevnetEntrypoint()
    account.nonce = entrypoint.recall_account_nonce(account.address)

    abi = Abi.load(sandbox / "adder.abi.json")
    sc_controller = entrypoint.create_smart_contract_controller(abi)

    transaction = sc_controller.create_transaction_for_deploy(
        sender=account,
        nonce=account.nonce,
        bytecode=bytecode_path,
        gas_limit=GAS_LIMIT_DEPLOY,
        arguments=[0]
    )

    hash = entrypoint.send_transaction(transaction)
    print("See transaction:")
    print(f"{EXPLORER_URL}/transactions/{hash.hex()}")

    address_computer = AddressComputer()
    contract_address = address_computer.compute_contract_address(account.address, transaction.nonce)

    print("Contract address:")
    print(f"{EXPLORER_URL}/accounts/{contract_address.to_bech32()}")


def add(args: Any):
    contract_address = Address.new_from_bech32(args.contract)
    value = args.value

    signer = pick_a_signer()
    account = Account(signer.secret_key)

    entrypoint = DevnetEntrypoint()
    account.nonce = entrypoint.recall_account_nonce(account.address)

    abi = Abi.load(sandbox / "adder.abi.json")
    sc_controller = entrypoint.create_smart_contract_controller(abi)

    transaction = sc_controller.create_transaction_for_execute(
        sender=account,
        nonce=account.nonce,
        contract=contract_address,
        function="add",
        gas_limit=GAS_LIMIT_ADD,
        arguments=[value]
    )

    hash = entrypoint.send_transaction(transaction)
    print("See transaction:")
    print(f"{EXPLORER_URL}/transactions/{hash.hex()}")


def get_sum(args: Any):
    contract_address = Address.new_from_bech32(args.contract)

    entrypoint = DevnetEntrypoint()

    abi = Abi.load(sandbox / "adder.abi.json")
    sc_controller = entrypoint.create_smart_contract_controller(abi)

    query = sc_controller.create_query(
        contract=contract_address,
        function="getSum",
        arguments=[]
    )

    response = sc_controller.run_query(query)

    value = sc_controller.parse_query_response(response)[0]

    print("Return code:", response.return_code)
    print("Return message:", response.return_message)
    print("Sum:", value)


if __name__ == "__main__":
    main(sys.argv[1:])
