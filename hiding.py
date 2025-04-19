"""
This module provides functionality for securely hiding files by:
- Moving original files to hidden files with obfuscated names.
- Storing mappings of original_file_path and hidden_file_path in an encrypted database.
- Creating shortcuts for easy access to hidden files.

Usage:
    python hiding.py --file_path <file_path>  # Hides a specific file
    python hiding.py --testbed                # Hides all files in the testbed folder
"""


import os
import sys
import json
import random
import argparse
from dataclasses import dataclass

import win32com.client

from modules.aes import AESCipher
from modules.utils import get_dir_path, load_json, load_encrypted_data
from modules.linker_utils import ext2app, hash_name, name_gen, postprocessing


@dataclass
class MappingDB:
    """
    A data class to hold information in the enc_mapping.dll(mapping.db).

    Attributes:
        hidden_ext_list (list): List of supported file extensions for hiding.
        hidden_dir_dict (dict): Dictionary of hidden directories.
        mapping_dict (dict): Mapping of hidden file paths to their original names.
        hash_table (dict): Mapping of hashed names to hidden file paths.
    """
    hidden_ext_list: list
    hidden_dir_dict: dict
    mapping_dict: dict
    hash_table: dict


DIR_PATH = get_dir_path()
MAPPING_DB = MappingDB(list(), dict(), dict(), dict())
APP_PATH_DB = load_json(os.path.join(DIR_PATH, "db", "app_path.dll"))


def preprocessing() -> dict[str, str]:
    """
    Prepares and validates the environment for file hiding.

    Returns:
        dict: A dictionary mapping file extensions to their corresponding icon paths.
    """
    for key in list(MAPPING_DB.hidden_dir_dict.keys()):
        if not os.path.exists(MAPPING_DB.hidden_dir_dict.get(key)):
            print(f"[-] {key} directory doesn't exist.")
            MAPPING_DB.hidden_dir_dict.pop(key)

    ext_icon_dict = {}
    for key in list(APP_PATH_DB.keys()):
        app = APP_PATH_DB.get(key)
        if not os.path.exists(app.get("path", "")):
            print(f"[-] {key} application doesn't exist.")
            APP_PATH_DB.pop(key)
        else:
            for ext in app.get("ext", []):
                ext_icon_dict[ext] = os.path.join(DIR_PATH, "icon", app.get("ico", ""))
    print("[*] Supported Extensions:", ext_icon_dict.keys())
    return ext_icon_dict


def make_shortcut(file_path: str, ext_icon_dict: dict[str, str], hidden_dir_key: str = "") -> str | None:
    """
    Hides a file by creating a shortcut to it.

    Args:
        file_path (str): The path of the file to be hidden.
        ext_icon_dict (dict): Extension-to-icon mapping.
        hidden_dir_key (str): The key of the directory for hidden files. If not provided, a random key is chosen.

    Returns:
        Optional[str]: The path of the hidden file, or None if hiding failed.
    """
    ext = file_path.split(".")[-1].lower()
    if ext not in ext_icon_dict:
        print(f"[-] Failed to hide {file_path}. Extension {ext} is not supported.")
        return None
    app_path = ext2app(ext, APP_PATH_DB)
    if not app_path:
        print(f"[-] Failed to hide {file_path}. No application path found for the extension: {ext}.")
        return None

    new_name = name_gen(MAPPING_DB.hidden_ext_list)
    if not hidden_dir_key:
        hidden_dir_key = random.choice(list(MAPPING_DB.hidden_dir_dict.keys()))
    hidden_file_path = os.path.join(MAPPING_DB.hidden_dir_dict.get(hidden_dir_key), new_name)
    shortcut_path = f"{file_path}.lnk"
    hashed_name = hash_name(hidden_file_path)

    try:
        os.rename(file_path, hidden_file_path)
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)

        # python script (for test)
        shortcut.Targetpath = "python"
        shortcut.Arguments = f"\"{DIR_PATH}\\linker.py\" --hash {hashed_name}"
        # executable (for release)
        if getattr(sys, "frozen", False):
            shortcut.Targetpath = os.path.join(DIR_PATH, "dist", "linker.exe")
            shortcut.Arguments = f"--hash {hashed_name}"

        shortcut.IconLocation = ext_icon_dict.get(ext, "")
        shortcut.Save()

        MAPPING_DB.mapping_dict[hidden_file_path] = file_path
        MAPPING_DB.hash_table[hashed_name] = hidden_file_path

        print(f"[+] Hiding success: {file_path} -> {hidden_file_path}")
        return hidden_file_path

    except Exception as e:
        print(f"[-] Failed to hide {file_path}: {e}")
        return None


def synchronize(target_list: list[str], mapping_dict: dict[str, str]) -> None:
    """
    Synchronizes hidden files with their corresponding shortcuts.

    Args:
        target_list (list): List of hidden file paths.
        mapping_dict (dict): Mapping of hidden files to their original files.
    """
    for hidden_file in target_list:
        original_file = mapping_dict.get(hidden_file)
        shortcut_path = f"{original_file}.lnk"
        if os.path.exists(hidden_file) and os.path.exists(shortcut_path):
            file_st = os.stat(hidden_file)
            os.utime(shortcut_path, (file_st.st_atime, file_st.st_mtime))


def main(file_path: str = "", is_test: bool = False) -> None:
    """
    Main function to hide files by creating shortcuts and managing file mappings.

    Args:
        file_path (str): Path of the file to hide. If None, hides all files in the testbed folder.
        is_test (bool): Whether to hide all files in the testbed folder.
    """
    aes = AESCipher()

    enc_mapping_filepath = os.path.join(DIR_PATH, "db", "enc_mapping.dll")
    raw_data, pw = load_encrypted_data(enc_mapping_filepath, aes, prompt="PASSWORD? : ")
    data = json.loads(raw_data.replace("'", '"'))

    MAPPING_DB.hidden_ext_list = data["hidden_ext"]
    MAPPING_DB.hidden_dir_dict = data["hidden_dir"]
    MAPPING_DB.mapping_dict = data["mapping_table"]
    MAPPING_DB.hash_table = data["hash_table"]

    ext_icon_dict = preprocessing()

    if is_test:
        target_path = os.path.join(DIR_PATH, "testbed")
        if not os.path.exists(target_path):
            print("[-] Testbed folder does not exist.")
            sys.exit(1)
        target_list = []
        for file in os.listdir(target_path):
            file_path = os.path.join(target_path, file)
            # "help" is hardcoded as the hidden_dir_key for testing purposes
            target_list.append(make_shortcut(file_path, ext_icon_dict, hidden_dir_key="help")) 
    else:
        target_list = [make_shortcut(file_path, ext_icon_dict)]

    data["mapping_table"] = MAPPING_DB.mapping_dict
    data["hash_table"] = MAPPING_DB.hash_table
    postprocessing(data, aes, pw, enc_mapping_filepath)
    synchronize(target_list, MAPPING_DB.mapping_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", type=str, help="Hide specific file (provide full path)")
    parser.add_argument("--testbed", action="store_true", help="Hide all files in testbed folder")
    args = parser.parse_args()

    if not (args.file_path or args.testbed):
        raise ValueError("[-] Usage: hiding.py --file_path OR --testbed <file_path>")

    main(args.file_path, args.testbed)
