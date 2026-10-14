import unittest
from campusflow.reports import get_work_queue

class TestReports(unittest.TestCase):
    
    def test_work_queue_sorting(self):
        messy_tickets = [
            {"id": "T003", "priority": "low", "status": "open"},
            {"id": "T001", "priority": "critical", "status": "in_progress"},
            {"id": "T010", "priority": "critical", "status": "open"},
            {"id": "T002", "priority": "critical", "status": "open"},
            {"id": "T004", "priority": "high", "status": "resolved"}
        ]
        
        sorted_queue = get_work_queue(messy_tickets)
        
        # Only open tickets appear; in_progress and resolved are strictly excluded
        self.assertEqual(len(sorted_queue), 3)
        # Order: critical before low, and earlier numeric ID (T002 before T010)
        self.assertEqual(sorted_queue[0]["id"], "T002")
        self.assertEqual(sorted_queue[1]["id"], "T010")
        self.assertEqual(sorted_queue[2]["id"], "T003")

    def test_generate_report_counts(self):
        from campusflow.reports import generate_report
        
        tickets = [
            {"id": "T001", "category": "Network", "priority": "high", "status": "open"},
            {"id": "T002", "category": "Hardware", "priority": "high", "status": "in_progress"},
            {"id": "T003", "category": "Network", "priority": "low", "status": "resolved"}
        ]
        
        report = generate_report(tickets)
        
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["by_status"]["in_progress"], 1)
        self.assertEqual(report["by_status"]["resolved"], 1)
        self.assertEqual(report["by_priority"]["high"], 2)
        self.assertEqual(report["by_priority"]["low"], 1)
        self.assertEqual(report["by_category"]["Network"], 2)
        self.assertEqual(report["by_category"]["Hardware"], 1)
        self.assertEqual(report["unresolved"], 2)  # open + in_progress
        self.assertEqual(report["resolved"], 1)
        self.assertAlmostEqual(report["resolution_percentage"], 33.33, places=1)
        
    def test_generate_report_zero_tickets(self):
        """10. Empty report returns 0%, no crash."""
        from campusflow.reports import generate_report
        
        report = generate_report([])
        
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["by_status"], {})
        self.assertEqual(report["by_priority"], {})
        self.assertEqual(report["by_category"], {})
        self.assertEqual(report["unresolved"], 0)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)

    def test_report_counts_with_fixture_after_resolve_and_reopen(self):
        """11. Report counts agree with known fixture after resolve and reopen."""
        from campusflow.reports import generate_report
        
        tickets = [
            {"id": "T001", "category": "Software", "priority": "critical", "status": "open"},
            {"id": "T002", "category": "Network", "priority": "high", "status": "open"},
            {"id": "T003", "category": "Other", "priority": "medium", "status": "open"}
        ]
        
        # Initial: 3 total, 3 unresolved, 0 resolved, 0%
        r1 = generate_report(tickets)
        self.assertEqual(r1["unresolved"], 3)
        self.assertEqual(r1["resolved"], 0)
        self.assertEqual(r1["resolution_percentage"], 0.0)

        # Resolve T001: 2 unresolved, 1 resolved, 33.3%
        tickets[0]["status"] = "resolved"
        r2 = generate_report(tickets)
        self.assertEqual(r2["unresolved"], 2)
        self.assertEqual(r2["resolved"], 1)
        self.assertAlmostEqual(r2["resolution_percentage"], 33.33, places=1)

        # Resolve T002: 1 unresolved, 2 resolved, 66.7%
        tickets[1]["status"] = "resolved"
        r3 = generate_report(tickets)
        self.assertEqual(r3["unresolved"], 1)
        self.assertEqual(r3["resolved"], 2)
        self.assertAlmostEqual(r3["resolution_percentage"], 66.67, places=1)

        # Reopen T001 to open: 2 unresolved, 1 resolved, 33.3% (no double-counting)
        tickets[0]["status"] = "open"
        r4 = generate_report(tickets)
        self.assertEqual(r4["unresolved"], 2)
        self.assertEqual(r4["resolved"], 1)
        self.assertEqual(r4["by_status"]["open"], 2)
        self.assertEqual(r4["by_status"]["resolved"], 1)

# This must always be at the very bottom, un-indented!
if __name__ == '__main__':
    unittest.main()