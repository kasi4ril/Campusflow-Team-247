import unittest
from campusflow.workflow import assign_ticket

class TestWorkflow(unittest.TestCase):
    
    def setUp(self):
        # setUp runs before every single test. 
        # We create a fake "database" (a list of dictionaries) to test against.
        self.mock_tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi down",
                "status": "open",
                "assigned_to": None
            }
        ]

    def test_assign_ticket_success(self):
        # 1. Arrange: We have our mock tickets from setUp.
        
        # 2. Act: We call the function we are ABOUT to build.
        updated_ticket = assign_ticket(self.mock_tickets, "T001", "Grace Hopper")
        
        # 3. Assert: We prove the function did what it was supposed to do.
        self.assertEqual(updated_ticket["assigned_to"], "Grace Hopper")

if __name__ == '__main__':
    unittest.main()