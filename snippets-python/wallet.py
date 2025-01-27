import getpass
import os
from pathlib import Path
from typing import List, Tuple
from multiversx_sdk import UserSigner

from constants import HRP


def pick_a_signer() -> UserSigner:
    entries: List[Path] = []

    folder = Path(os.environ["SANDBOX"])
    pem_files = sorted(folder.glob("*.pem"))
    json_files = sorted(set(folder.glob("*.json")) - set(folder.glob("*.abi.json")))

    for pem_file in pem_files:
        entries.append(pem_file)
    for json_file in json_files:
        entries.append(json_file)

    for i, path in enumerate(entries):
        print(f"{i}: {path}")

    choice = int(input("Pick a signer: "))
    path = entries[choice]

    signer = create_signer_from_file(path)
    return signer


def create_signer_from_file(path: Path):
    if path.suffix == ".pem":
        return UserSigner.from_pem_file(path)
    elif path.suffix == ".json":
        password = getpass.getpass("Password: ")
        return UserSigner.from_wallet(path, password)
    else:
        raise Exception("Unknown wallet type.")
