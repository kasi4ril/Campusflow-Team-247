import unittest
from campusflow.tickets import calculate_priority, create_ticket

class TestTickets(unittest.TestCase):

    def test_priority_rules(self):
        # RULE 1: High + 12 -> critical
        self.assertEqual(calculate_priority("high", 12), "critical")
        # RULE 2: High + 2 -> high
        self.assertEqual(calculate_priority("high", 2), "high")
        # RULE 3: Low + 4 -> medium
        self.assertEqual(calculate_priority("low", 4), "medium")
        # RULE 4: Low + 1 -> low
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_reject_zero_affected_users(self):
        with self.assertRaises(ValueError):
            calculate_priority("high", 0)

    def test_reject_blank_title(self):
        tickets = []
        with self.assertRaises(ValueError):
            create_ticket(tickets, "   ", "Network", "high", 5)

    def test_reject_invalid_category(self):
        tickets = []
        with self.assertRaises(ValueError):
            create_ticket(tickets, "Server crash", "Cloud", "high", 5)

    def test_create_ticket_auto_id(self):
        tickets = []
        t1 = create_ticket(tickets, "Wi-Fi down", "Network", "high", 15)
        self.assertEqual(t1["id"], "T001")
        self.assertEqual(t1["priority"], "critical")
        
        t2 = create_ticket(tickets, "Mouse broken", "Hardware", "low", 1)
        self.assertEqual(t2["id"], "T002")
        self.assertEqual(len(tickets), 2)

if __name__ == '__main__':
    unittest.main()