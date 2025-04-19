"""
Utility functions for the hiding, linking, and recovery.

Functions:
- ext2app: Maps file extensions to their corresponding applications.
- hash_name: Generates a SHA-1 hash for a given string.
- name_gen: Creates unique file names with obfuscated extensions.
- postprocessing: Encrypts and writes mapping data to a file.
"""

import json
import random
import string
import hashlib
from typing import Any


def ext2app(ext: str, app_path_db: dict[str, dict[str, Any]]) -> str:
    """
    Maps a file extension to the corresponding application path.

    Args:
        ext (str): The file extension (e.g., 'txt', 'jpg').
        app_path_dict (dict): A dictionary mapping application names
                              to their properties, including supported extensions.

    Returns:
        str: The path to the application associated with the given extension, 
             or an empty string if not found.
    """
    for info in app_path_db.values():
        if ext in info.get("ext", []):
            return info.get("path", "")
    return ""


def hash_name(name: str) -> str:
    """
    Generates a SHA-1 hash for a given string.

    Args:
        name (str): The input string to hash.

    Returns:
        str: The hexadecimal SHA-1 hash of the input string.
    """
    sha = hashlib.new('sha1')
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
    name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    ext = random.choice(hidden_ext_list)
    return f"{name}.{ext}"


def postprocessing(data_dict: dict[str, Any], aes, pw: str, db_filepath: str) -> None:
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
    with open(db_filepath, "w", encoding="utf-8") as f:
        f.write(enc_data)
