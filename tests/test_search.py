"""
Tests for search and combined filtering module (Engineer B).
TDD Step 1: Red Phase - Defining search specifications.
"""
import unittest
from campusflow.search import search_tickets

class TestSearch(unittest.TestCase):

    def setUp(self):
        self.sample_tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi router offline in Library",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
                "notes": []
            },
            {
                "id": "T002",
                "title": "Laptop keyboard key broken",
                "category": "Hardware",
                "urgency": "low",
                "affected_users": 1,
                "priority": "low",
                "status": "in_progress",
                "assigned_to": "Grace Hopper",
                "notes": []
            },
            {
                "id": "T003",
                "title": "Faculty Wi-Fi connection slow",
                "category": "Network",
                "urgency": "medium",
                "affected_users": 5,
                "priority": "medium",
                "status": "open",
                "assigned_to": "Ada Lovelace",
                "notes": []
            },
            {
                "id": "T010",
                "title": "Campus Wi-Fi guest portal issue",
                "category": "Network",
                "urgency": "high",
                "affected_users": 12,
                "priority": "critical",
                "status": "resolved",
                "assigned_to": "Grace Hopper",
                "notes": []
            }
        ]

    def test_search_title_case_insensitive_substring(self):
        """08. Search title ignores case, matching substring using casefold."""
        # Query in uppercase matching mixed-case titles (case-insensitive with same punctuation)
        results = search_tickets(self.sample_tickets, title="WI-FI")
        self.assertEqual(len(results), 3)
        result_ids = [t["id"] for t in results]
        self.assertIn("T001", result_ids)
        self.assertIn("T003", result_ids)
        self.assertIn("T010", result_ids)
        self.assertNotIn("T002", result_ids)

        # Query in lowercase with punctuation
        results_dash = search_tickets(self.sample_tickets, title="wi-fi")
        self.assertEqual(len(results_dash), 3)

        # Partial substring match
        results_sub = search_tickets(self.sample_tickets, title="keyboard")
        self.assertEqual(len(results_sub), 1)
        self.assertEqual(results_sub[0]["id"], "T002")

    def test_search_title_case_insensitive(self):
        """T08 contract test alias: Substring match on title ignores case."""
        self.test_search_title_case_insensitive_substring()

    def test_combined_search_filters_logical_and(self):
        """09. Combined search filters use logical AND (all supplied must match)."""
        # Title "wi-fi" + category "Network" + status "open"
        # T001 matches (Network, open, wi-fi)
        # T003 matches (Network, open, wi-fi)
        # T010 does NOT match because status is resolved
        results = search_tickets(
            self.sample_tickets,
            title="wi-fi",
            category="Network",
            status="open"
        )
        self.assertEqual(len(results), 2)
        result_ids = [t["id"] for t in results]
        self.assertListEqual(sorted(result_ids), ["T001", "T003"])

        # Add priority filter: only critical open network wi-fi
        results_critical = search_tickets(
            self.sample_tickets,
            title="wi-fi",
            category="Network",
            status="open",
            priority="critical"
        )
        self.assertEqual(len(results_critical), 1)
        self.assertEqual(results_critical[0]["id"], "T001")

    def test_combined_search_filters_and_logic(self):
        """T09 contract test alias: Multi-filter search requires ALL supplied filters to match."""
        self.test_combined_search_filters_logical_and()


    def test_search_empty_filters_ignored(self):
        """Empty or whitespace filters are ignored (do not restrict results)."""
        # Empty title and None category
        results = search_tickets(self.sample_tickets, title="  ", category="", status="in_progress")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "T002")

        # All empty filters returns a copy of all tickets
        all_results = search_tickets(self.sample_tickets)
        self.assertEqual(len(all_results), 4)

    def test_search_does_not_mutate_records(self):
        """Search is strictly read-only and must not modify ticket records or list."""
        import copy
        snapshot = copy.deepcopy(self.sample_tickets)
        _ = search_tickets(self.sample_tickets, title="wi-fi", category="Network")
        self.assertEqual(self.sample_tickets, snapshot)

    def test_search_optional_sorting_by_priority_and_numeric_id(self):
        """Search results can be sorted by priority then numeric ID without altering work queue."""
        results = search_tickets(self.sample_tickets, category="Network", sort_results=True)
        self.assertEqual(len(results), 3)
        # T001 (critical) and T010 (critical) before T003 (medium)
        # Ties between T001 and T010: numeric ID 1 before 10
        self.assertEqual(results[0]["id"], "T001")
        self.assertEqual(results[1]["id"], "T010")
        self.assertEqual(results[2]["id"], "T003")

    def test_search_no_matches_returns_empty_list(self):
        """Returns empty list when no tickets match criteria."""
        results = search_tickets(self.sample_tickets, title="printer jam")
        self.assertEqual(results, [])

if __name__ == "__main__":
    unittest.main()
