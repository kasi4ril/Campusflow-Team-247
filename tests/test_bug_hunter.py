import unittest
from copy import deepcopy

from campusflow.reports import get_work_queue


class TestBugHunterEngineerAChecksB(unittest.TestCase):
    def test_bug_hunter_engineer_a_checks_b(self):
        tickets = [
            {"id": "T010", "priority": "high", "status": "open"},
            {"id": "T002", "priority": "high", "status": "open"},
            {"id": "T001", "priority": "low", "status": "resolved"},
        ]
        original_tickets = deepcopy(tickets)

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T010"],
        )
        self.assertEqual(
            tickets,
            original_tickets,
            "Building the work queue must not change the original tickets.",
        )


if __name__ == "__main__":
    unittest.main()
