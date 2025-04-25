"""
This module handles the recovery of files that were previously hidden.
It renames obfuscated files back to their original names and removes
associated shortcuts.

Usage:
    python recovery.py --hash <hashed_filename>         # Recover a file using its hashed_filename
    python recovery.py --link_file_path <shortcut.lnk>  # Recover a file using its shortcut
    python recovery.py --all                            # Recover all hidden files
"""

import os
import sys
import json
import argparse

import pylnk3

from modules.aes import AESCipher
from modules.common_utils import get_dir_path
from modules.security_utils import hash_name, postprocessing, load_encrypted_data


def recovery(hidden_file: str, mapping_dict: dict[str, str],
             hash_table: dict[str, str], shortcut_file_path: str = None) -> None:
    """
    Recovers a hidden file to its original location and removes its associated shortcut.

    Args:
        hidden_file (str): Path to the hidden file.
        mapping_dict (dict): Mapping of hidden file paths to their original file paths.
        hash_table (dict): Mapping of hashed names to hidden file paths.
        shortcut_file_path (str): Path of the shortcut file for restoring the original file.
    """
    try:
        if shortcut_file_path:
            original_file = shortcut_file_path.removesuffix(".lnk")
        else:
            original_file = mapping_dict.get(hidden_file)
        if not original_file:
            raise ValueError(f"No mapping found for {hidden_file}.")

        os.rename(hidden_file, original_file)
        shortcut_path = f"{original_file}.lnk"
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)

        mapping_dict.pop(hidden_file, None)
        h_name = hash_name(hidden_file)
        hash_table.pop(h_name, None)
        print(f"  [+] Recovered: {hidden_file} -> {original_file}")

    except (ValueError, OSError) as e:
        print(f"  [-] Failed to recover {hidden_file}: {e}")


def main(hashed_name: str | None = None, shortcut_file_path: str | None = None,
         recover_all: bool | None = False) -> None:
    """
    Main function to recover hidden files based on their hash or recover all hidden files.

    Args:
        hashed_name (str): The hashed name of the file to recover.
        shortcut_file_path (str): Path of the shortcut file for restoring the original file.
        recover_all (bool): Flag to indicate recovery of all hidden files.
    """
    aes = AESCipher()

    enc_mapping_filepath = os.path.join(get_dir_path(), "db", "enc_mapping.dll")
    raw_data, pw = load_encrypted_data(enc_mapping_filepath, aes, prompt="PASSWORD? : ")
    data = json.loads(raw_data.replace("'", '"'))

    mapping_dict = data.get("mapping_table")
    hash_table = data.get("hash_table")

    if recover_all:
        if not mapping_dict:
            print("[-] No hidden files to recover.")
            sys.exit(1)

        hidden_files = list(mapping_dict.keys())
        for hidden_file in hidden_files:
            recovery(hidden_file, mapping_dict, hash_table)
    else:
        if hashed_name in hash_table:
            hidden_file = hash_table.get(hashed_name)
            recovery(hidden_file, mapping_dict, hash_table, shortcut_file_path)
        else:
            print("[-] Provided hash not found.")
            sys.exit(1)

    data["mapping_table"] = mapping_dict
    data["hash_table"] = hash_table
    postprocessing(data, aes, pw, enc_mapping_filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hash", type=str, help="Recover specific file using its hash.")
    parser.add_argument("--link_file_path", type=str, help="The path of the .lnk shortcut file.")
    parser.add_argument("--all", action="store_true", help="Recover all hidden files.")

    args = parser.parse_args()

    if not any([args.hash, args.link_file_path, args.all]):
        print("[-] No arguments provided.")
        print("[*] Usage: recover.py --all OR --hash <hash> OR --link_file_path <link_file_path>")
        sys.exit(1)

    if sum([bool(args.hash), bool(args.link_file_path), bool(args.all)]) > 1:
        print("[-] Only one of --all, --hash, or --link_file_path can be used at a time.")
        sys.exit(1)

    if args.hash:
        print(f"[+] Recovering file with hash: {args.hash}\m")

    elif args.link_file_path:
        if not (os.path.isfile(args.link_file_path)
                and args.link_file_path.lower().endswith(".lnk")):
            print(f"[!] Invalid shortcut file: {args.link_file_path}")
            sys.exit(1)

        try:
            lnk = pylnk3.parse(args.link_file_path)
            if lnk.arguments and lnk.arguments.startswith("--hash"):
                args.hash = lnk.arguments.split()[1]
            else:
                raise ValueError("Invalid or missing hash in shortcut.")

        except (ValueError, pylnk3.FormatException) as e:
            print(f"[!] Error processing shortcut: {e}")
            sys.exit(1)

        print(f"[+] Recovering file with link file: {args.link_file_path}\n")

    elif args.all:
        print("[*] Recovering all hidden files...\n")

    main(args.hash, args.link_file_path, args.all)
