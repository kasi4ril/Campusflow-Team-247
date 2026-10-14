"""
Tests for CLI Engineering Understanding Check module (Engineer B).
TDD Step 1: Red Phase.
"""
import unittest
from campusflow.understanding_check import (
    QUESTIONS,
    validate_choice,
    score_quiz,
    run_understanding_check
)

class TestUnderstandingCheck(unittest.TestCase):

    def test_question_bank_completeness(self):
        """Question bank must contain all 6 mandatory scenario questions with A/B/C/D options."""
        self.assertEqual(len(QUESTIONS), 6)
        for q in QUESTIONS:
            self.assertIn("id", q)
            self.assertIn("prompt", q)
            self.assertIn("options", q)
            self.assertIn("correct_answer", q)
            self.assertIn(q["correct_answer"], ["A", "B", "C", "D"])
            self.assertEqual(set(q["options"].keys()), {"A", "B", "C", "D"})

    def test_validate_choice(self):
        """14. Validates A/B/C/D input and rejects invalid choices."""
        self.assertEqual(validate_choice("a"), "A")
        self.assertEqual(validate_choice("B"), "B")
        self.assertEqual(validate_choice(" c "), "C")
        self.assertEqual(validate_choice("d"), "D")

        # Invalid choices
        self.assertIsNone(validate_choice("E"))
        self.assertIsNone(validate_choice("1"))
        self.assertIsNone(validate_choice(""))
        self.assertIsNone(validate_choice("yes"))

    def test_score_quiz_calculation(self):
        """14. Quiz scoring awards 1 point per correct answer."""
        perfect_answers = {
            1: "B",
            2: "C",
            3: "B",
            4: "C",
            5: "C",
            6: "B"
        }
        self.assertEqual(score_quiz(perfect_answers), 6)

        half_answers = {
            1: "B",  # correct
            2: "A",  # incorrect
            3: "B",  # correct
            4: "A",  # incorrect
            5: "C",  # correct
            6: "D"   # incorrect
        }
        self.assertEqual(score_quiz(half_answers), 3)

        zero_answers = {1: "A", 2: "A", 3: "A", 4: "A", 5: "A", 6: "A"}
        self.assertEqual(score_quiz(zero_answers), 0)

    def test_run_understanding_check_with_retry_and_explanations(self):
        """Test simulated CLI session with retry on invalid input and explanation capture."""
        # User enters 'Z' (invalid), then 'B' for Q1; 'C' for Q2; 'B' for Q3;
        # 'C' for Q4; 'C' for Q5; 'B' for Q6.
        # Then two explanations.
        simulated_inputs = [
            "Z",   # invalid Q1 retry
            "B",   # Q1 valid
            "C",   # Q2
            "B",   # Q3
            "C",   # Q4
            "C",   # Q5
            "B",   # Q6
            "Unassigned tickets cannot be in progress because work requires an assigned staff owner.",  # Explanation 1
            "Zero tickets cannot divide by zero, so 0% resolution must be handled defensively."        # Explanation 2
        ]
        input_iter = iter(simulated_inputs)
        printed_messages = []

        def mock_input(prompt=""):
            return next(input_iter)

        def mock_print(*args, **kwargs):
            printed_messages.append(" ".join(str(a) for a in args))

        score, explanations = run_understanding_check(
            input_func=mock_input,
            print_func=mock_print,
            save_to_file=False
        )

        self.assertEqual(score, 6)
        self.assertEqual(len(explanations), 2)
        # Verify invalid choice re-prompted
        self.assertTrue(any("Invalid choice" in msg for msg in printed_messages))

if __name__ == "__main__":
    unittest.main()
