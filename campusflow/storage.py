"""
Storage Module

Handles saving and loading the ticket database to a JSON file.
"""
import json
import os

# We define the default path here so it's easy to change later
DEFAULT_FILE_PATH = "data/tickets.json"

def load_tickets(file_path=DEFAULT_FILE_PATH):
    """
    Loads tickets from a JSON file.
    If the file doesn't exist, returns an empty list.
    If the file is corrupted, raises a ValueError.
    """
    if not os.path.exists(file_path):
        # Rule: Missing file allows a fresh start
        return []

    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Rule: Malformed JSON must produce a clear error, not silently erase data
        raise ValueError("CRITICAL: The tickets.json file is corrupted. Fix or delete it manually.")


def save_tickets(tickets, file_path=DEFAULT_FILE_PATH):
    """
    Saves the list of tickets to a JSON file.
    """
    dir_name = os.path.dirname(file_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(file_path, "w") as file:
        # indent=4 makes the JSON file human-readable!
        json.dump(tickets, file, indent=4)