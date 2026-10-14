"""
Follow-up Notes Module for CampusFlow Next.

Handles note creation, per-ticket sequential ID generation,
and enforces lifecycle invariants (only open or in_progress tickets accept notes).
"""

def generate_note_id(ticket):
    """
    Generates the next sequential unique note ID for a ticket (e.g. 'N001', 'N002').
    """
    notes = ticket.get("notes") or []
    max_num = 0
    for n in notes:
        nid = n.get("note_id", "")
        if isinstance(nid, str) and nid.startswith("N") and nid[1:].isdigit():
            max_num = max(max_num, int(nid[1:]))
    return f"N{max_num + 1:03d}"


def add_note(ticket, author, message):
    """
    Validates inputs and adds a follow-up note to an open or in_progress ticket.

    Args:
        ticket (dict): The ticket dictionary to update.
        author (str): Non-empty staff member or user name.
        message (str): 5-300 character message.

    Returns:
        dict: The created note dictionary.

    Raises:
        ValueError: If ticket is resolved, author is blank, or message length is invalid.
    """
    if ticket.get("status") == "resolved":
        raise ValueError("Cannot add note: Resolved tickets cannot accept notes unless reopened to open.")

    if not author or not str(author).strip():
        raise ValueError("Note author cannot be blank.")

    cleaned_msg = str(message).strip() if message else ""
    if len(cleaned_msg) < 5 or len(cleaned_msg) > 300:
        raise ValueError(f"Note message must be between 5 and 300 characters (got {len(cleaned_msg)}).")

    if "notes" not in ticket or not isinstance(ticket["notes"], list):
        ticket["notes"] = []

    note_id = generate_note_id(ticket)
    new_note = {
        "note_id": note_id,
        "author": str(author).strip(),
        "message": cleaned_msg
    }

    ticket["notes"].append(new_note)
    return new_note

