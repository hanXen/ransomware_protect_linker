"""
Security-related utility functions.

Functions:
- hash_name: Generates a SHA-1 hash for a given string.
- name_gen: Creates unique file names with obfuscated extensions.
- get_verified_password: Prompts the user for a password with optional confirmation.
- load_encrypted_data: Decrypts and loads data from an encrypted file.
- postprocessing: Encrypts and writes mapping data to a file.
"""

import sys
import json
import random
import string
import hashlib
import getpass

from modules.aes import AESCipher
from modules.common_utils import read_file, write_file


def hash_name(name: str) -> str:
    """
    Generates a SHA-1 hash for a given string.

    Args:
        name (str): The input string to hash.

    Returns:
        str: The hexadecimal SHA-1 hash of the input string.
    """
    sha = hashlib.new("sha1")
    sha.update(name.encode())
    return sha.hexdigest()


def name_gen(hidden_ext_list: list[str], length: int = 8) -> str:
    """
    Generates a random file name with a random extension from the provided list.

    Args:
        hidden_ext_list (list): A list of possible file extensions.
        length (int): The length of the randomly generated name (default is 8).

    Returns:
        str: A randomly generated file name with an extension.
    """
    name = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    ext = random.choice(hidden_ext_list)
    return f"{name}.{ext}"


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
    try:
        if confirm:
            pw = getpass.getpass("Enter PASSWORD : ")
            pw2 = getpass.getpass("Confirm PASSWORD : ")
            if not pw or pw != pw2:
                print("[-] PASSWORD ERROR")
                sys.exit(1)
        else:
            pw = getpass.getpass("PASSWORD? : ")
        return pw
    except (KeyboardInterrupt, EOFError):
        print("\n[!] Keyboard Interrupt")
        sys.exit(1)


def load_encrypted_data(filepath: str, aes: AESCipher,
                        prompt: str = "PASSWORD? : ") -> tuple[str, str]:
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
        except (KeyboardInterrupt, EOFError):
            print("\n[!] Keyboard Interrupt")
            sys.exit(1)
        try:
            dec_data = aes.decrypt(data, pw)
            if "hidden_ext" in dec_data or "mapping_table" in dec_data:
                return dec_data, pw
        except UnicodeDecodeError:
            print("[-] PASSWORD Fail :(")


def postprocessing(data_dict: dict[str, str | list], aes, pw: str, db_filepath: str) -> None:
    """
    Encrypts and writes a dictionary to a specified file path.

    Args:
        data_dict (dict): The dictionary to encrypt and write.
        aes: An instance of the AES cipher for encryption.
        pw (str): The password used for encryption.
        db_filepath (str): The file path where the encrypted data will be stored.

    Returns:
        None
    """
    enc_data = aes.encrypt(json.dumps(data_dict), pw)
    write_file(db_filepath, enc_data)
