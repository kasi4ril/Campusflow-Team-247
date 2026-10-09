import unittest
from campusflow.reports import get_work_queue

class TestReports(unittest.TestCase):
    
    def test_work_queue_sorting(self):
        messy_tickets = [
            {"id": "T003", "priority": "low", "status": "open"},
            {"id": "T001", "priority": "critical", "status": "in_progress"},
            {"id": "T002", "priority": "critical", "status": "open"},
            {"id": "T004", "priority": "high", "status": "resolved"}
        ]
        
        sorted_queue = get_work_queue(messy_tickets)
        
        self.assertEqual(len(sorted_queue), 3)
        self.assertEqual(sorted_queue[0]["id"], "T001")
        self.assertEqual(sorted_queue[1]["id"], "T002")
        self.assertEqual(sorted_queue[2]["id"], "T003")

    def test_generate_report_counts(self):
        from campusflow.reports import generate_report
        
        tickets = [
            {"id": "T001", "priority": "high", "status": "open"},
            {"id": "T002", "priority": "high", "status": "open"},
            {"id": "T003", "priority": "low", "status": "resolved"}
        ]
        
        report = generate_report(tickets)
        
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["by_status"]["open"], 2)
        self.assertEqual(report["by_status"]["resolved"], 1)
        self.assertEqual(report["by_priority"]["high"], 2)
        
    def test_generate_report_zero_tickets(self):
        from campusflow.reports import generate_report
        
        report = generate_report([])
        
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["by_status"], {})

# This must always be at the very bottom, un-indented!
if __name__ == '__main__':
    unittest.main()