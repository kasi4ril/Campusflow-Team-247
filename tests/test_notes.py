"""
Tests for Follow-up Notes Module.
Covers Contract Scenarios T05, T06, T07, and ID generation invariants.
"""
import unittest
from copy import deepcopy

from campusflow.notes import add_note, generate_note_id
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, update_status


class TestNotes(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        self.ticket = create_ticket(
            self.tickets,
            "Internet connection lost",
            "Network",
            "high",
            5,
        )
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

    def test_generate_note_id(self):
        """Sequential per-ticket note ID generation."""
        self.assertEqual(generate_note_id({"notes": []}), "N001")
        self.assertEqual(
            generate_note_id({"notes": [{"note_id": "N004"}]}),
            "N005",
        )
        self.assertEqual(
            generate_note_id({"notes": [{"note_id": "N001"}, {"note_id": "N009"}]}),
            "N010",
        )

    def test_add_valid_note(self):
        """05. Valid note added and note ID correct (T05)."""
        first = add_note(self.ticket, "Grace Hopper", "Router restarted")
        second = add_note(self.ticket, "Alan Turing", "Cable checked")

        self.assertEqual(first["note_id"], "N001")
        self.assertEqual(second["note_id"], "N002")
        self.assertEqual(len(self.ticket["notes"]), 2)

    def test_notes_receive_sequential_ids(self):
        """Alias for T05 sequential note IDs."""
        self.test_add_valid_note()

    def test_invalid_note_preserves_id_counter(self):
        """06. Blank/too-short note rejected without consuming ID (T06)."""
        original = deepcopy(self.ticket)

        # Blank author
        with self.assertRaises(ValueError):
            add_note(self.ticket, "   ", "Router restarted")
        self.assertEqual(self.ticket, original)

        # Message too short (< 5 chars)
        with self.assertRaises(ValueError):
            add_note(self.ticket, "Grace Hopper", "No")
        self.assertEqual(self.ticket, original)

        # Message too long (> 300 chars)
        with self.assertRaises(ValueError):
            add_note(self.ticket, "Grace Hopper", "x" * 301)
        self.assertEqual(self.ticket, original)

        # Note counter not consumed; next valid note gets N001
        note = add_note(self.ticket, "Grace Hopper", "Router restarted")
        self.assertEqual(note["note_id"], "N001")

    def test_failed_note_does_not_change_ticket_or_consume_id(self):
        """Alias for T06 failed note state preservation."""
        self.test_invalid_note_preserves_id_counter()

    def test_note_on_resolved_ticket_lifecycle(self):
        """07. Note on resolved ticket rejected; note after reopen accepted (T07)."""
        assign_ticket(self.tickets, self.ticket["id"], "Grace Hopper")
        update_status(self.tickets, self.ticket["id"], "in_progress")
        update_status(self.tickets, self.ticket["id"], "resolved")

        original = deepcopy(self.ticket)

        # Rejection on resolved ticket
        with self.assertRaises(ValueError):
            add_note(self.ticket, "Grace Hopper", "Checked the router")
        self.assertEqual(self.ticket, original)

        # Acceptance after reopening to open
        update_status(self.tickets, self.ticket["id"], "open")
        note = add_note(self.ticket, "Grace Hopper", "Checked the router")
        self.assertEqual(note["note_id"], "N001")

    def test_resolved_ticket_requires_reopening_before_note(self):
        """Alias for T07 lifecycle."""
        self.test_note_on_resolved_ticket_lifecycle()


if __name__ == "__main__":
    unittest.main()
