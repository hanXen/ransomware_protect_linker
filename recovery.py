"""
This module handles the recovery of files that were previously hidden.
It renames obfuscated files back to their original names and removes
associated shortcuts.

Usage:
    python recovery.py --hash <hashed_file_name>  # Recover a specific file
    python recovery.py --all                      # Recover all hidden files
"""


import os
import sys
import json
import argparse

from modules.aes import AESCipher
from modules.utils import get_dir_path, load_encrypted_data
from modules.linker_utils import hash_name, postprocessing


def recovery(hidden_file: str, mapping_dict: dict, hash_table: dict) -> None:
    """
    Recovers a hidden file to its original location and removes its associated shortcut.

    Args:
        hidden_file (str): Path to the hidden file.
        mapping_dict (Dict[str, str]): Mapping of hidden file paths to their original file paths.
        hash_table (Dict[str, str]): Mapping of hashed names to hidden file paths.
    """
    try:
        original_file = mapping_dict[hidden_file]
        os.rename(hidden_file, original_file)
        shortcut_path = f"{original_file}.lnk"
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
        mapping_dict.pop(hidden_file, None)
        h_name = hash_name(hidden_file)
        hash_table.pop(h_name, None)
        print(f"[+] Recovered: {hidden_file} -> {original_file}")

    except Exception as e:
        print(f"[-] Failed to recover {hidden_file}: {e}")


def main(hashed_name: str = "", recover_all: bool = False):
    """
    Main function to recover hidden files based on their hash or recover all hidden files.

    Args:
        hashed_name (str): The hashed name of the file to recover.
        recover_all (bool): Flag to indicate recovery of all hidden files.
    """
    aes = AESCipher()

    enc_mapping_filepath = os.path.join(get_dir_path(), "db", "enc_mapping.dll")
    raw_data, pw = load_encrypted_data(enc_mapping_filepath, aes, prompt="PASSWORD? : ")
    data = json.loads(raw_data.replace("'", '"'))

    mapping_dict = data['mapping_table']
    hash_table = data['hash_table']

    if recover_all:
        for hidden_file in list(mapping_dict.keys()):
            recovery(hidden_file, mapping_dict, hash_table)
    else:
        if hashed_name in hash_table:
            hidden_file = hash_table.get(hashed_name)
            recovery(hidden_file, mapping_dict, hash_table)
        else:
            print("[-] Provided hash not found.")
            sys.exit(1)

    data['mapping_table'] = mapping_dict
    data['hash_table'] = hash_table
    postprocessing(data, aes, pw, enc_mapping_filepath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hash', type=str, help="Recover specific file using its hash")
    parser.add_argument('--all', action='store_true', help="Recover all hidden files")
    args = parser.parse_args()

    if not (args.hash or args.all):
        raise ValueError("[-] Usage: recover.py --all OR --hash <hash>")

    main(args.hash, args.all)
