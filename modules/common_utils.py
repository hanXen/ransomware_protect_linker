"""
Utils for common operations.

Functions:
- get_dir_path: Retrieves the base directory path for the current environment.
- read_file: Reads the content of a file.
- write_file: Writes data to a file.
- load_json: Loads and parses JSON data from a file.
- ext_to_app_path: Maps file extensions to their corresponding applications.
"""

import os
import sys
import json

from filelock import FileLock


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
    lock = FileLock(f"{filepath}.lock")
    with lock:
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
    lock = FileLock(f"{filepath}.lock")
    with lock:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(data)


def load_json(filepath: str) -> dict[str, list | dict | str]:
    """
    Loads JSON data from a file.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict: The parsed JSON data.
    """
    lock = FileLock(f"{filepath}.lock")
    with lock:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)


def ext_to_app_path(ext: str, app_path_db: dict[str, dict[str, list | str]]) -> str:
    """
    Maps a file extension to the corresponding application path.

    Args:
        ext (str): The file extension (e.g., "txt", "jpg").
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
