"""
Storage Module

Validates ticket records and safely loads and saves the JSON database.
"""

import json
import os
import re
import tempfile

from campusflow.validation import (
    validate_title,
    validate_category,
    validate_urgency,
    validate_affected_users,
)


DEFAULT_FILE_PATH = "data/tickets.json"


def _expected_priority(urgency, affected_users):
    """Calculate the required priority for a validated ticket."""
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def validate_ticket_record(ticket, seen_ids=None):
    """Validate a complete ticket record or raise ValueError."""
    if seen_ids is None:
        seen_ids = set()

    if not isinstance(ticket, dict):
        raise ValueError("Each ticket record must be a JSON object.")

    required = {
        "id",
        "title",
        "category",
        "urgency",
        "affected_users",
        "priority",
        "status",
        "assigned_to",
        "notes",
    }

    missing = required - ticket.keys()
    if missing:
        raise ValueError(f"Ticket is missing required fields: {sorted(missing)}")

    if set(ticket.keys()) - required:
        raise ValueError("Unauthorized fields in ticket record")

    ticket_id = ticket["id"]
    if not isinstance(ticket_id, str) or not re.fullmatch(r"T\d{3,}", ticket_id):
        raise ValueError("Ticket ID must look like T001.")

    if ticket_id in seen_ids:
        raise ValueError(f"Duplicate ticket ID: {ticket_id}")

    try:
        validate_title(ticket["title"])
        canonical_category = validate_category(ticket["category"])
        canonical_urgency = validate_urgency(ticket["urgency"])
        affected_users = validate_affected_users(ticket["affected_users"])
    except (TypeError, ValueError) as error:
        raise ValueError(f"Invalid ticket {ticket_id}: {error}") from error

    if ticket["title"] != ticket["title"].strip():
        raise ValueError("Ticket title must not contain surrounding whitespace.")

    if ticket["category"] != canonical_category:
        raise ValueError("Ticket category must use its canonical spelling.")

    if ticket["urgency"] != canonical_urgency:
        raise ValueError("Ticket urgency must be lower-case.")

    expected_priority = _expected_priority(canonical_urgency, affected_users)
    if ticket["priority"] != expected_priority:
        raise ValueError(f"Ticket priority must be {expected_priority}.")

    status = ticket["status"]
    if not isinstance(status, str) or status not in {
        "open", "in_progress", "resolved"
    }:
        raise ValueError("Ticket status is invalid.")

    assignee = ticket["assigned_to"]
    if assignee is not None and (
        not isinstance(assignee, str) or not assignee.strip()
    ):
        raise ValueError("Assignee must be a nonblank string or None.")

    if ticket["status"] == "in_progress" and not (
        isinstance(assignee, str) and assignee.strip()
    ):
        raise ValueError("An in-progress ticket must have an assignee.")

    notes = ticket["notes"]
    if not isinstance(notes, list):
        raise ValueError("Ticket notes must be a list.")

    note_ids = set()
    for note in notes:
        if not isinstance(note, dict):
            raise ValueError("Each note must be a JSON object.")

        if not {"note_id", "author", "message"} <= note.keys():
            raise ValueError("Each note requires note_id, author, and message.")

        note_id = note["note_id"]
        if not isinstance(note_id, str) or not re.fullmatch(r"N\d{3,}", note_id):
            raise ValueError("Note ID must look like N001.")

        if note_id in note_ids:
            raise ValueError(f"Duplicate note ID: {note_id}")

        if not isinstance(note["author"], str) or not note["author"].strip():
            raise ValueError("Note author must not be blank.")

        message = note["message"]
        if not isinstance(message, str) or not 5 <= len(message.strip()) <= 300:
            raise ValueError("Note message must contain 5 to 300 characters.")

        note_ids.add(note_id)

    seen_ids.add(ticket_id)
    return ticket


def load_tickets(file_path=DEFAULT_FILE_PATH):
    """Load and validate every record before returning any tickets."""
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            records = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError("The tickets JSON file is corrupted.") from error

    if not isinstance(records, list):
        raise ValueError("The tickets JSON root must be a list.")

    validated = []
    seen_ids = set()

    for record in records:
        validate_ticket_record(record, seen_ids)
        validated.append(record)

    return validated


def save_tickets(tickets, file_path=DEFAULT_FILE_PATH):
    """Validate tickets and atomically replace the JSON file."""
    if not isinstance(tickets, list):
        raise ValueError("Tickets must be provided as a list.")

    seen_ids = set()
    for ticket in tickets:
        validate_ticket_record(ticket, seen_ids)

    directory = os.path.dirname(os.path.abspath(file_path))
    os.makedirs(directory, exist_ok=True)

    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=directory,
            prefix=".tickets-",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = temporary_file.name
            json.dump(tickets, temporary_file, indent=4)
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        os.replace(temporary_path, file_path)
    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)
