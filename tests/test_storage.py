import unittest
import os
import json

from campusflow.storage import save_tickets, load_tickets


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.test_file = "data/test_tickets.json"
        os.makedirs(os.path.dirname(self.test_file), exist_ok=True)

        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def make_ticket(self, ticket_id="T001"):
        return {
            "id": ticket_id,
            "title": "Broken mouse",
            "category": "Hardware",
            "urgency": "medium",
            "affected_users": 1,
            "priority": "medium",
            "status": "open",
            "assigned_to": None,
            "notes": [
                {
                    "note_id": "N001",
                    "author": "Grace Hopper",
                    "message": "Checked the mouse cable",
                }
            ],
        }

    def test_missing_file_returns_empty_list(self):
        self.assertEqual(load_tickets(self.test_file), [])

    def test_save_and_load_preserves_data(self):
        mock_tickets = [self.make_ticket()]
        save_tickets(mock_tickets, self.test_file)

        loaded_tickets = load_tickets(self.test_file)

        self.assertEqual(loaded_tickets, mock_tickets)

    def test_corrupted_json_raises_error(self):
        with open(self.test_file, "w", encoding="utf-8") as file:
            file.write("this is not json { [ bad data")

        with self.assertRaises(ValueError):
            load_tickets(self.test_file)

    def test_t12_save_load_preserves_notes_and_ids(self):
        ticket = self.make_ticket()
        ticket["notes"].append(
            {
                "note_id": "N002",
                "author": "Alan Turing",
                "message": "Tested with another mouse",
            }
        )

        save_tickets([ticket], self.test_file)
        loaded = load_tickets(self.test_file)

        self.assertEqual(loaded[0]["id"], "T001")
        self.assertEqual(
            [note["note_id"] for note in loaded[0]["notes"]],
            ["N001", "N002"],
        )
        self.assertEqual(loaded[0]["notes"], ticket["notes"])

    def test_t13_duplicate_ticket_ids_are_rejected(self):
        duplicate_tickets = [
            self.make_ticket("T001"),
            self.make_ticket("T001"),
        ]

        with self.assertRaises(ValueError):
            save_tickets(duplicate_tickets, self.test_file)

    def test_t13_invalid_record_in_file_is_rejected(self):
        valid_ticket = self.make_ticket()
        invalid_ticket = self.make_ticket("T002")
        invalid_ticket["affected_users"] = 0

        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump([valid_ticket, invalid_ticket], file)

        with self.assertRaises(ValueError):
            load_tickets(self.test_file)

    def test_failed_load_does_not_return_partial_records(self):
        valid_ticket = self.make_ticket()
        invalid_ticket = self.make_ticket("T002")
        invalid_ticket["title"] = "   "

        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump([valid_ticket, invalid_ticket], file)

        with self.assertRaises(ValueError):
            load_tickets(self.test_file)

    def test_unauthorized_fields_are_rejected(self):
        ticket = self.make_ticket()
        ticket["admin"] = True

        with self.assertRaisesRegex(
            ValueError, "Unauthorized fields in ticket record"
        ):
            save_tickets([ticket], self.test_file)

    def test_invalid_status_type_raises_value_error(self):
        for invalid_status in ([], {}):
            with self.subTest(status=invalid_status):
                ticket = self.make_ticket()
                ticket["status"] = invalid_status

                with self.assertRaises(ValueError):
                    save_tickets([ticket], self.test_file)


if __name__ == "__main__":
    unittest.main()
