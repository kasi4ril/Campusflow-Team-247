import unittest
from campusflow.reports import get_work_queue

class TestReports(unittest.TestCase):
    
    def test_work_queue_sorting(self):
        # 1. Arrange: Create a messy list of tickets
        messy_tickets = [
            {"id": "T003", "priority": "low", "status": "open"},
            {"id": "T001", "priority": "critical", "status": "in_progress"},
            {"id": "T002", "priority": "critical", "status": "open"},
            {"id": "T004", "priority": "high", "status": "resolved"} # Should be ignored!
        ]
        
        # 2. Act: Ask our (soon to be built) function to sort them
        sorted_queue = get_work_queue(messy_tickets)
        
        # 3. Assert: 
        # It should only return 3 tickets (ignoring the resolved one)
        self.assertEqual(len(sorted_queue), 3)
        # The first ticket should be T001 (Critical, and older than T002)
        self.assertEqual(sorted_queue[0]["id"], "T001")
        # The second should be T002
        self.assertEqual(sorted_queue[1]["id"], "T002")
        # The third should be T003
        self.assertEqual(sorted_queue[2]["id"], "T003")

if __name__ == '__main__':
    unittest.main()