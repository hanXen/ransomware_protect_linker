"""
Utils for common operations.

Functions:
- get_dir_path: Retrieves the base directory path for the current environment.
- read_file: Reads the content of a file.
- write_file: Writes data to a file.
- load_json: Loads and parses JSON data from a file.
- get_verified_password: Prompts the user for a password with optional confirmation.
- load_encrypted_data: Decrypts and loads data from an encrypted file.
"""


import os
import sys
import json
import getpass
from typing import Dict, Tuple
from modules.aes import AESCipher


def get_dir_path() -> str:
    """
    Retrieves the base directory path of the current script or executable.

    Returns:
        str: The base directory path.
    """
    if getattr(sys, "frozen", False):  # When running as a bundled executable
        file_path = sys.executable
        file_name = os.path.basename(file_path)
        return file_path.split(f"\\dist\\{file_name}", maxsplit=1)[0]
    else:  # When running as a script
        file_path = os.path.abspath(__file__)
        return os.path.dirname(os.path.dirname(file_path))


def read_file(filepath: str) -> str:
    """
    Reads the content of a text file.

    Args:
        filepath (str): Path to the file.

    Returns:
        str: The content of the file.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write_file(filepath: str, data: str) -> None:
    """
    Writes data to a file.

    Args:
        filepath (str): Path to the file.
        data (str): Data to write to the file.

    Returns:
        None
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data)


def load_json(filepath: str) -> Dict:
    """
    Loads JSON data from a file.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        Dict: The parsed JSON data.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_verified_password(confirm: bool = False) -> str:
    """
    Prompts the user for a password, with an optional confirmation step.

    Args:
        confirm (bool): If True, requires the user to confirm the password.

    Returns:
        str: The verified password.

    Raises:
        SystemExit: If passwords do not match or are empty.
    """
    if confirm:
        pw = getpass.getpass("Enter PASSWORD : ")
        pw2 = getpass.getpass("Confirm PASSWORD : ")
        if not pw or pw != pw2:
            print("[-] PASSWORD ERROR")
    else:
        pw = getpass.getpass("PASSWORD? : ")
    return pw


def load_encrypted_data(filepath: str, aes: AESCipher, prompt: str = "PASSWORD? : ") -> Tuple[str, str]:
    """
    Loads and decrypts encrypted data from a file using a password.

    Args:
        filepath (str): Path to the encrypted file.
        aes (AESCipher): An instance of the AES cipher for decryption.
        prompt (str): The prompt to display for password input.

    Returns:
        Tuple[str, str]: The decrypted data and the password used for decryption.

    Raises:
        None: The function loops until a valid password is provided.
    """
    data = read_file(filepath)
    while True:
        try:
            pw = getpass.getpass(prompt)
        except (KeyboardInterrupt,EOFError):
            print("\n[!] Keyboard Interrupt")
            sys.exit(1)
            
        try:
            dec_data = aes.decrypt(data, pw)
            if "hidden_ext" in dec_data or "mapping_table" in dec_data:
                return dec_data, pw
        except Exception:
            print("[-] PASSWORD Fail :(")
