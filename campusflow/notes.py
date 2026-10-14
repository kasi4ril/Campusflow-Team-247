"""
Notes Module

Handles ticket notes, validation, and sequential note IDs.
"""


def add_note(ticket, author, message):
    """Add a validated note to a ticket without partial changes."""
    if ticket.get("status") == "resolved":
        raise ValueError("Cannot add notes to a resolved ticket. Reopen it first.")

    if not isinstance(author, str) or not author.strip():
        raise ValueError("Note author must not be blank.")

    if not isinstance(message, str):
        raise ValueError("Note message must be a string.")

    message = message.strip()
    if not 5 <= len(message) <= 300:
        raise ValueError("Note message must contain 5 to 300 characters.")

    existing_notes = ticket.get("notes", [])
    if not isinstance(existing_notes, list):
        raise ValueError("Ticket notes must be a list.")

    # Find the highest existing note number before creating a new ID.
    max_number = 0
    for note in existing_notes:
        note_id = note.get("note_id", "")
        if (
            isinstance(note_id, str)
            and note_id.startswith("N")
            and note_id[1:].isdigit()
        ):
            max_number = max(max_number, int(note_id[1:]))

    note = {
        "note_id": f"N{max_number + 1:03d}",
        "author": author.strip(),
        "message": message,
    }

    # Mutate the ticket only after all validation has succeeded.
    ticket.setdefault("notes", []).append(note)
    return note
