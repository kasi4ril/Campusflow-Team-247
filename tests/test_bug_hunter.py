"""
Bug Hunter Test Suite for CampusFlow Next.
BH-2: Authored by Engineer B (Shwarji Khatang) checking Engineer A's validation/storage/lifecycle invariants.
"""
import unittest
from copy import deepcopy

from campusflow.notes import add_note


class TestBugHunterEngineerBChecksA(unittest.TestCase):
    """
    BH-2: Engineer B tests Engineer A's validation, notes, and lifecycle edge cases.
    """

    def setUp(self):
        self.sample_ticket = {
            "id": "T001",
            "title": "Core network switch packet drops",
            "category": "Network",
            "urgency": "high",
            "affected_users": 25,
            "priority": "critical",
            "status": "open",
            "assigned_to": "Grace Hopper",
            "notes": []
        }

    def test_bug_hunter_engineer_b_checks_a(self):
        """
        BH-2: Engineer B checks Engineer A's validation and state-preservation invariants.

        Edge Case 1 (Whitespace Padding Boundary in Notes):
        A message containing whitespace padding whose raw string length is >= 5 (e.g. '   ok   ', len 8)
        must be evaluated on its stripped length. Since 'ok' is only 2 characters (< 5), it must be
        strictly rejected with ValueError without mutating ticket['notes'] or consuming note IDs.

        Edge Case 2 (Invariant I3 & I1 - when validation module is loaded):
        Verify boolean values for affected_users are rejected because isinstance(True, int) is True,
        and illegal direct status transitions (open -> resolved) or whitespace assignees are rejected.
        """
        snapshot = deepcopy(self.sample_ticket)

        # 1. Whitespace-padded short message rejection
        with self.assertRaises(ValueError):
            add_note(self.sample_ticket, "Engineer B", "   ok   ")

        # Invariance check: ticket['notes'] must remain empty and untouched
        self.assertEqual(
            self.sample_ticket,
            snapshot,
            "Failed note creation must leave ticket dictionary 100% unchanged."
        )

        # Subsequent valid note must still receive the very first note ID (N001)
        valid_note = add_note(self.sample_ticket, "Engineer B", "Investigating switch port buffer logs.")
        self.assertEqual(valid_note["note_id"], "N001")
        self.assertEqual(len(self.sample_ticket["notes"]), 1)

        # 2. Rejection of notes on resolved ticket without state mutation
        self.sample_ticket["status"] = "resolved"
        resolved_snapshot = deepcopy(self.sample_ticket)

        with self.assertRaises(ValueError):
            add_note(self.sample_ticket, "Engineer B", "Attempted follow-up on resolved ticket.")

        self.assertEqual(
            self.sample_ticket,
            resolved_snapshot,
            "Adding a note to a resolved ticket must raise ValueError and not alter notes list."
        )

        # 3. Dynamic check of Engineer A's centralized validation helpers (if available)
        try:
            from campusflow.validation import (
                validate_affected_users,
                can_transition,
                validate_title,
                validate_category
            )

            # Invariant I3: Reject booleans True and False for affected_users
            with self.assertRaises(ValueError):
                validate_affected_users(True)
            with self.assertRaises(ValueError):
                validate_affected_users(False)

            # Invariant I1: Illegal transition directly from open to resolved
            self.assertFalse(can_transition("open", "resolved", "Grace Hopper"))

            # Invariant I1: Open to in_progress with blank or whitespace assignee
            self.assertFalse(can_transition("open", "in_progress", None))
            self.assertFalse(can_transition("open", "in_progress", "   "))

            # Title validation: Blank or whitespace-only rejected
            with self.assertRaises(ValueError):
                validate_title("   ")

            # Canonical category normalization
            self.assertEqual(validate_category("network"), "Network")
            with self.assertRaises(ValueError):
                validate_category("Cloud")

        except ImportError:
            # When running on Engineer B's isolated branch prior to merge with Engineer A
            pass


if __name__ == "__main__":
    unittest.main()
