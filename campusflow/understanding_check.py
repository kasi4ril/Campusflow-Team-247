"""
Engineering Understanding Check Module for CampusFlow Next (Engineer B).

Implements an interactive scenario quiz testing application invariants,
defensive validation, combined filtering, and lifecycle rules.
Decouples question bank definitions from scoring and input validation logic.
"""

import os

QUESTIONS = [
    {
        "id": 1,
        "prompt": "Ticket T001 is open and unassigned. A user tries to move it to in_progress.",
        "options": {
            "A": "Accept",
            "B": "Reject and preserve all data",
            "C": "Resolve it automatically",
            "D": "Remove ticket"
        },
        "correct_answer": "B",
        "explanation": (
            "Work cannot begin on an unassigned ticket. Invariants require an assigned owner "
            "before entering in_progress, and rejected actions must preserve existing state completely."
        )
    },
    {
        "id": 2,
        "prompt": "The app has zero tickets. What should resolution percentage display?",
        "options": {
            "A": "Crash",
            "B": "100%",
            "C": "0%",
            "D": "Divide by one without explanation"
        },
        "correct_answer": "C",
        "explanation": (
            "An empty dataset must report 0.0% defensively without raising ZeroDivisionError."
        )
    },
    {
        "id": 3,
        "prompt": "Filter title='wifi', category='Network', status='open'. Which records should match?",
        "options": {
            "A": "Any record matching one filter",
            "B": "Only records matching all supplied filters",
            "C": "All network records",
            "D": "All open records"
        },
        "correct_answer": "B",
        "explanation": (
            "Combined search filters operate under strict logical AND; all non-empty criteria must match."
        )
    },
    {
        "id": 4,
        "prompt": "A resolved ticket receives 'Add note'. What should happen?",
        "options": {
            "A": "Append anyway",
            "B": "Delete old notes",
            "C": "Reject until reopened",
            "D": "Change status silently"
        },
        "correct_answer": "C",
        "explanation": (
            "Resolved tickets are immutable and cannot accept new notes or assignment changes "
            "unless explicitly reopened to open."
        )
    },
    {
        "id": 5,
        "prompt": "The JSON file includes two tickets with the same ID. What should load do?",
        "options": {
            "A": "Keep both",
            "B": "Replace memory with duplicates",
            "C": "Reject the load without changing current memory",
            "D": "Rename IDs silently"
        },
        "correct_answer": "C",
        "explanation": (
            "Safe storage enforces atomic validation. If any record violates uniqueness or integrity, "
            "load is rejected without wiping memory."
        )
    },
    {
        "id": 6,
        "prompt": "A PR changes validation but has no negative-case tests. Best review action?",
        "options": {
            "A": "Approve because it runs",
            "B": "Request focused tests and reasoning",
            "C": "Merge immediately",
            "D": "Ask AI to approve it"
        },
        "correct_answer": "B",
        "explanation": (
            "Peer review requires testing boundary and failure modes. Positive runs do not prove "
            "rejection invariants work."
        )
    }
]

def validate_choice(choice):
    """
    Validates user choice against allowed options (A, B, C, D).

    Args:
        choice: Raw input string.

    Returns:
        str: Normalized uppercase letter ('A', 'B', 'C', 'D') or None if invalid.
    """
    if not choice or not isinstance(choice, str):
        return None
    cleaned = choice.strip().upper()
    if cleaned in ["A", "B", "C", "D"]:
        return cleaned
    return None

def score_quiz(user_answers):
    """
    Calculates total score from submitted answers.

    Args:
        user_answers (dict): Mapping of {question_id: choice_letter}.

    Returns:
        int: Number of correct answers (0 to 6).
    """
    correct_count = 0
    for q in QUESTIONS:
        qid = q["id"]
        if user_answers.get(qid) == q["correct_answer"]:
            correct_count += 1
    return correct_count

def run_understanding_check(input_func=input, print_func=print, save_to_file=True):
    """
    Runs the interactive Engineering Understanding Check CLI.

    Args:
        input_func: Callable for reading user input (defaults to built-in input).
        print_func: Callable for printing output (defaults to built-in print).
        save_to_file (bool): Whether to persist recorded explanations to disk.

    Returns:
        tuple: (score, explanations_dict)
    """
    print_func("\n" + "=" * 50)
    print_func("      CampusFlow Engineering Understanding Check")
    print_func("=" * 50)
    print_func("Answer 6 scenario questions regarding system invariants.\n")

    user_answers = {}

    for q in QUESTIONS:
        print_func(f"\n[Scenario Q{q['id']}/6]")
        print_func(q["prompt"])
        for opt in ["A", "B", "C", "D"]:
            print_func(f"  {opt}. {q['options'][opt]}")

        while True:
            raw = input_func("Your answer (A/B/C/D): ")
            choice = validate_choice(raw)
            if choice:
                user_answers[q["id"]] = choice
                break
            print_func("Invalid choice! Please enter A, B, C, or D.")

    score = score_quiz(user_answers)
    print_func("\n" + "-" * 50)
    print_func(f"Quiz Complete! Your Score: {score}/6")
    print_func("-" * 50)

    # Prompt for written explanation of at least two answers
    print_func("\nEngineering Reflection: Provide a short code/invariant explanation for at least 2 questions.")
    explanations = {}

    for qid in [1, 2]:
        q_obj = next(q for q in QUESTIONS if q["id"] == qid)
        print_func(f"\nExplain Q{qid}: {q_obj['prompt']}")
        exp = input_func("Explanation: ").strip()
        explanations[qid] = exp

    if save_to_file:
        os.makedirs("docs", exist_ok=True)
        file_path = "docs/quiz-responses.md"
        with open(file_path, "a") as f:
            f.write(f"\n## Understanding Check Submission (Score: {score}/6)\n")
            for qid, exp in explanations.items():
                f.write(f"- **Q{qid} Selected:** {user_answers.get(qid)}\n")
                f.write(f"  **Explanation:** {exp}\n")

    return score, explanations
