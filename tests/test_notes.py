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

    def test_generate_note_id(self):
        self.assertEqual(generate_note_id({"notes": []}), "N001")
        self.assertEqual(
            generate_note_id({"notes": [{"note_id": "N004"}]}),
            "N005",
        )

    def test_add_valid_note(self):
        self.test_notes_receive_sequential_ids()

    def test_notes_receive_sequential_ids(self):
        first = add_note(self.ticket, "Grace Hopper", "Router restarted")
        second = add_note(self.ticket, "Alan Turing", "Cable checked")

        self.assertEqual(first["note_id"], "N001")
        self.assertEqual(second["note_id"], "N002")
        self.assertEqual(len(self.ticket["notes"]), 2)

    def test_invalid_note_preserves_id_counter(self):
        self.test_failed_note_does_not_change_ticket_or_consume_id()

    def test_failed_note_does_not_change_ticket_or_consume_id(self):
        original = deepcopy(self.ticket)

        with self.assertRaises(ValueError):
            add_note(self.ticket, "   ", "Router restarted")

        self.assertEqual(self.ticket, original)

        with self.assertRaises(ValueError):
            add_note(self.ticket, "Grace Hopper", "No")

        self.assertEqual(self.ticket, original)

        with self.assertRaises(ValueError):
            add_note(self.ticket, "Grace Hopper", "x" * 301)

        self.assertEqual(self.ticket, original)

        note = add_note(self.ticket, "Grace Hopper", "Router restarted")
        self.assertEqual(note["note_id"], "N001")

    def test_note_on_resolved_ticket_lifecycle(self):
        self.test_resolved_ticket_requires_reopening_before_note()

    def test_resolved_ticket_requires_reopening_before_note(self):
        assign_ticket(self.tickets, self.ticket["id"], "Grace Hopper")
        update_status(self.tickets, self.ticket["id"], "in_progress")
        update_status(self.tickets, self.ticket["id"], "resolved")

        original = deepcopy(self.ticket)

        with self.assertRaises(ValueError):
            add_note(self.ticket, "Grace Hopper", "Checked the router")

        self.assertEqual(self.ticket, original)

        update_status(self.tickets, self.ticket["id"], "open")
        note = add_note(self.ticket, "Grace Hopper", "Checked the router")
        self.assertEqual(note["note_id"], "N001")


if __name__ == "__main__":
    unittest.main()
