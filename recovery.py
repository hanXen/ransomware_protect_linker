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
import shutil
import argparse
import subprocess

import pylnk3

from modules.aes import AESCipher
from modules.common_utils import get_dir_path
from modules.security_utils import hash_name, postprocessing, load_encrypted_data


def process_link_file(link_file_path: str) -> str:
    """
    Processes a .lnk shortcut file to extract the hashed name.

    Args:
        link_file_path (str): Path of the shortcut file.

    Returns:
        str: Extracted hashed name from the shortcut file.

    Raises:
        ValueError: If the shortcut file is invalid or missing a hash.
        pylnk3.FormatException: If the shortcut file format is invalid.
    """
    try:
        lnk = pylnk3.parse(link_file_path)
        if lnk.arguments and lnk.arguments.split()[-2].startswith("--hash"):
            return lnk.arguments.split()[-1]
        else:
            raise ValueError("Invalid or missing hash in shortcut.")
    except (OSError, ValueError, pylnk3.FormatException) as e:
        print(f"[!] Error processing shortcut: {e}")
        print(f"Error File path: {link_file_path}")


def find_lnks_with_hash():
    """
    Searches for .lnk files with '--hash' in their target arguments across drives.

    Returns:
        list: Paths to matching .lnk files, or None if none are found.
    Raises:
        Exception: For unexpected errors.
    Notes:
        - Excludes "AppData" from the home directory search.
        - Dynamically scans drives D: to Z: and the user's home directory.
        - Uses PowerShell for efficient file discovery.
    """
    print("[*] Searching for all link files to recover....\n")
    try:
        user_home_dir = os.path.expanduser("~")
        appdata_path = os.path.join(user_home_dir, "AppData")
        drives = [f"{drive}:\\" for drive in "DEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{drive}:\\")]
        drives.insert(0,user_home_dir) if os.path.exists(user_home_dir) else None
        found_links = []

        for drive in drives:
            exclude_clause = ""
            if drive == user_home_dir:
                exclude_clause = f"Where-Object {{ $_.FullName -notlike '{appdata_path}*' }} |"
            powershell_command = f"""
                $Shell = New-Object -ComObject WScript.Shell
                Get-ChildItem -Path "{drive}" -Filter "*.lnk" -Recurse -ErrorAction SilentlyContinue |
                {exclude_clause}
                ForEach-Object {{
                    try {{
                        $Shortcut = $Shell.CreateShortcut($_.FullName)
                        if ($Shortcut.Arguments -like '*--hash*') {{
                            Write-Output $_.FullName
                        }}
                    }} catch {{ }}
                }}
            """
            result = subprocess.run(['powershell', '-Command', powershell_command], capture_output=True, text=True)
            if result.stdout:
                found_links.extend(result.stdout.strip().splitlines())

        if found_links:
            return found_links
        else:
            print("[-] No .lnk files with '--hash' in their target were found.")
    except Exception as e:
        print("[!] An error occured: \n", e)
    return None


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

        original_name, original_ext = os.path.splitext(original_file)
        count = 1
        while os.path.exists(original_file):
            original_file = f"{original_name}({count}){original_ext}"
            count += 1

        shutil.move(hidden_file, original_file)

        shortcut_path = f"{original_name}{original_ext}.lnk"
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

        found_lnk_files = find_lnks_with_hash()
        if not found_lnk_files:
            print("\n[*] Recovering all hidden files to the original paths.")
            hidden_files = list(mapping_dict.keys())
            for hidden_file in hidden_files:
                recovery(hidden_file, mapping_dict, hash_table)
        else:
            for lnk_file in found_lnk_files:
                hashed_name = process_link_file(lnk_file)
                hidden_file = hash_table.get(hashed_name)
                if not hidden_file:
                    continue
                recovery(hidden_file, mapping_dict, hash_table, lnk_file)

    else:
        if shortcut_file_path:
            hashed_name = process_link_file(shortcut_file_path)
            if not hashed_name:
                sys.exit(1)

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
        print(f"[+] Recovering file with hash: {args.hash}\n")

    elif args.link_file_path:
        if not (os.path.isfile(args.link_file_path)
                and args.link_file_path.lower().endswith(".lnk")):
            print(f"[!] Invalid shortcut file: {args.link_file_path}")
            sys.exit(1)

        print(f"[+] Recovering file with link file: {args.link_file_path}\n")

    elif args.all:
        print("[*] Recovering all hidden files...\n")

    main(args.hash, args.link_file_path, args.all)
