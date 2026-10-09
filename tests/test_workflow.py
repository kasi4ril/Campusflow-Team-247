import unittest
from campusflow.workflow import assign_ticket

class TestWorkflow(unittest.TestCase):
    
    def setUp(self):
        self.mock_tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi down",
                "status": "open",
                "assigned_to": None
            }
        ]

    def test_assign_ticket_success(self):
        updated_ticket = assign_ticket(self.mock_tickets, "T001", "Grace Hopper")
        self.assertEqual(updated_ticket["assigned_to"], "Grace Hopper")

    def test_unassigned_ticket_cannot_be_in_progress(self):
        with self.assertRaises(ValueError):
            from campusflow.workflow import update_status
            update_status(self.mock_tickets, "T001", "in_progress")

    def test_valid_ticket_lifecycle(self):
        from campusflow.workflow import assign_ticket, update_status
        
        # 1. Assign the ticket first so it is legal to move it
        assign_ticket(self.mock_tickets, "T001", "Ada Lovelace")
        
        # 2. Move it to in_progress
        ticket = update_status(self.mock_tickets, "T001", "in_progress")
        self.assertEqual(ticket["status"], "in_progress")
        
        # 3. Move it to resolved
        ticket = update_status(self.mock_tickets, "T001", "resolved")
        self.assertEqual(ticket["status"], "resolved")

# This must always be at the very bottom, completely un-indented!
if __name__ == '__main__':
    unittest.main()