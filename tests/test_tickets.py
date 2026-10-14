import unittest

from campusflow.tickets import calculate_priority, create_ticket


class TestTickets(unittest.TestCase):

    def test_priority_rules(self):
        self.assertEqual(calculate_priority("high", 12), "critical")
        self.assertEqual(calculate_priority("high", 2), "high")
        self.assertEqual(calculate_priority("low", 4), "medium")
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_reject_invalid_affected_users(self):
        invalid_values = [0, -1, 3.5, "five", True, False, None]

        for value in invalid_values:
            with self.subTest(affected_users=value):
                with self.assertRaises(ValueError):
                    calculate_priority("high", value)

    def test_reject_blank_title(self):
        tickets = []
        with self.assertRaises(ValueError):
            create_ticket(tickets, "   ", "Network", "high", 5)

        self.assertEqual(tickets, [])

    def test_reject_invalid_category(self):
        tickets = []
        with self.assertRaises(ValueError):
            create_ticket(tickets, "Server crash", "Cloud", "high", 5)

        self.assertEqual(tickets, [])

    def test_create_ticket_auto_id(self):
        tickets = []
        t1 = create_ticket(tickets, "Wi-Fi down", "Network", "high", 15)

        self.assertEqual(t1["id"], "T001")
        self.assertEqual(t1["priority"], "critical")

        t2 = create_ticket(tickets, "Mouse broken", "Hardware", "low", 1)

        self.assertEqual(t2["id"], "T002")
        self.assertEqual(len(tickets), 2)


if __name__ == "__main__":
    unittest.main()
