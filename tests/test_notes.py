"""
Tests for Follow-up Notes Module.
TDD Step 1: Red Phase for follow-up notes specifications.
"""
import unittest
from campusflow.notes import add_note, generate_note_id

class TestNotes(unittest.TestCase):

    def setUp(self):
        self.open_ticket = {
            "id": "T001",
            "title": "Wi-Fi outage in Lab 1",
            "category": "Network",
            "urgency": "high",
            "affected_users": 10,
            "priority": "critical",
            "status": "open",
            "assigned_to": "Grace Hopper",
            "notes": []
        }
        self.resolved_ticket = {
            "id": "T002",
            "title": "Mouse replacement",
            "category": "Hardware",
            "urgency": "low",
            "affected_users": 1,
            "priority": "low",
            "status": "resolved",
            "assigned_to": "Ada Lovelace",
            "notes": [
                {"note_id": "N001", "author": "Ada Lovelace", "message": "Replaced USB mouse."}
            ]
        }

    def test_add_valid_note(self):
        """05. Valid note added and note ID correct."""
        note = add_note(self.open_ticket, "Mentor A", "Router power cycle initiated.")
        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(note["author"], "Mentor A")
        self.assertEqual(note["message"], "Router power cycle initiated.")
        self.assertEqual(len(self.open_ticket["notes"]), 1)

        # Add second note
        note2 = add_note(self.open_ticket, "Mentor B", "Checking fiber uplink port.")
        self.assertEqual(note2["note_id"], "N002")
        self.assertEqual(len(self.open_ticket["notes"]), 2)

    def test_invalid_note_preserves_id_counter(self):
        """06. Blank/too-short note rejected without consuming ID."""
        # Blank author
        with self.assertRaises(ValueError):
            add_note(self.open_ticket, "   ", "Valid message text here.")
        self.assertEqual(len(self.open_ticket["notes"]), 0)

        # Message too short (< 5 chars)
        with self.assertRaises(ValueError):
            add_note(self.open_ticket, "Mentor A", "Hi")
        self.assertEqual(len(self.open_ticket["notes"]), 0)

        # Message too long (> 300 chars)
        with self.assertRaises(ValueError):
            add_note(self.open_ticket, "Mentor A", "A" * 301)
        self.assertEqual(len(self.open_ticket["notes"]), 0)

        # Next valid note must still receive N001 (ID counter not consumed)
        valid_note = add_note(self.open_ticket, "Mentor A", "Initial diagnostic complete.")
        self.assertEqual(valid_note["note_id"], "N001")

    def test_note_on_resolved_ticket_lifecycle(self):
        """07. Note on resolved ticket rejected; note after reopen accepted."""
        # Attempt to add note on resolved ticket must fail
        with self.assertRaises(ValueError):
            add_note(self.resolved_ticket, "Mentor A", "Attempting update on resolved ticket.")
        self.assertEqual(len(self.resolved_ticket["notes"]), 1)  # unchanged

        # Reopen ticket to open
        self.resolved_ticket["status"] = "open"
        # Now note must succeed and receive N002
        new_note = add_note(self.resolved_ticket, "Mentor A", "Reopened for follow-up testing.")
        self.assertEqual(new_note["note_id"], "N002")
        self.assertEqual(len(self.resolved_ticket["notes"]), 2)

    def test_generate_note_id_empty_and_existing(self):
        """generate_note_id generates sequential per-ticket IDs."""
        ticket = {"notes": []}
        self.assertEqual(generate_note_id(ticket), "N001")

        ticket["notes"].append({"note_id": "N001"})
        ticket["notes"].append({"note_id": "N009"})
        self.assertEqual(generate_note_id(ticket), "N010")

if __name__ == "__main__":
    unittest.main()

