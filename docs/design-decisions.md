# Design Decisions and Function Contracts: Progressive Architecture

This document tracks the architectural progression of CampusFlow from its initial prototype into CampusFlow Next and beyond.

---

# Part 1: Sprint 1 Baseline Architecture (CampusFlow v1)

## 1. Data Storage and Passing
- **Storage:** The ticket collection is stored in memory as a Python list of dictionaries.
- **Passing:** This list is initialized in `main.py` and passed as an argument to functions in other modules (e.g., `workflow.py`, `reports.py`) whenever they need to read or modify the data. Global variables will not be used.

## 2. Handling Invalid Input and Display
- **Signaling Errors:** Business logic functions will raise standard Python exceptions (e.g., `ValueError` for bad data, `KeyError` for unfound tickets) when input is invalid.
- **CLI Display:** The CLI menu in `main.py` will use `try/except` blocks to catch these exceptions and print a clean, user-friendly error message rather than crashing the program.

## 3. Expected Return Values
- **Creation/Updates:** Functions that create, update, or assign a ticket will return the modified ticket dictionary.
- **Queries:** Functions that fetch data (like the queue or reports) will return a list or a formatted summary.

## 4. JSON Persistence Ownership
- **Ownership:** The `storage.py` module owns all file I/O operations (`load_tickets` and `save_tickets`).
- **Usage:** `main.py` will call `load_tickets()` at application startup. To prevent data loss on unexpected exits, `main.py` will call `save_tickets()` immediately after any function that successfully modifies the ticket list.

## 5. Testing Business Logic
- **Separation of Concerns:** No `input()` or `print()` statements will be used inside the business logic modules (`tickets.py`, `workflow.py`, `reports.py`).
- **Testability:** All required data (like `ticket_id`, `staff_name`) will be passed as arguments. This allows the `unittest` framework to pass test data directly into the functions without requiring human interaction.

---

# Part 2: Sprint 2 Architecture & Invariants (CampusFlow Next v2)

## 6. Centralized Validation & Type-Defensive Programming
- **Rationale:** Validation logic in v1 was scattered inside `create_ticket` and `calculate_priority`. Sprint 2 introduces centralized validation helpers in `campusflow/validation.py` to validate title, category, urgency, and affected users uniformly.
- **Boolean Guard:** Because `bool` is a subclass of `int` in Python (`isinstance(True, int)` is `True`), the validator explicitly disallows booleans for `affected_users` (`type(affected_users) is bool` raises `ValueError`).

## 7. Status Lifecycle Guards & Invariants
- **Legal Transitions:** `open` → `in_progress` (strictly requires `assigned_to` to be a non-empty string), `in_progress` → `resolved`, and `resolved` → `open` (reopening).
- **Immutability of Resolved Records:** A ticket in `resolved` state is locked; it cannot receive assignment changes, status mutations (other than reopening), or follow-up notes.
- **Validate-Before-Mutate:** If a status change or assignment is invalid, the ticket dictionary and collection remain 100% unaltered.

## 8. Follow-up Notes Engine
- **Data Model:** Notes are stored in `ticket["notes"]` as a list of dictionaries (`{"note_id": "N001", "author": str, "message": str}`).
- **Scoping & ID Continuity:** Note IDs are sequential per ticket (`N001`, `N002`, ...). Rejected note creations (e.g. invalid length <5 or >300 characters, blank author) do not increment the note ID counter.
- **Lifecycle Bound:** Notes can only be added when ticket status is `open` or `in_progress`. Notes are preserved through `resolved` and reopen transitions.

## 9. Search & Filter Composition
- **Casefold Matching:** Title searches use Python's `.casefold()` for robust caseless substring matching.
- **Logical AND:** When combining title search with optional filters (category, status, priority), all supplied filters must evaluate to `True`. Empty filters are ignored.
- **Read-Only Guarantee:** The search module produces a new filtered list of tickets without modifying any existing ticket objects.

## 10. Atomic JSON Loading & State Safety
- **Validation Before Memory Replacement:** `load_tickets` decodes JSON and validates every record (structure, required keys, allowed status/category/urgency values, note shapes, and ID uniqueness).
- **State Preservation:** If ANY record is corrupted, malformed, or duplicates an existing ID, the load raises a `ValueError` immediately without overwriting the current in-memory ticket list.
- **ID Continuity:** After reload, next ticket and note IDs continue sequentially from the highest existing numeric ID, preventing ID collisions.

## 11. Engineering Understanding Check Separation
- **Question Bank vs Scoring Logic:** In `campusflow/understanding_check.py`, question data is decoupled from the CLI input loop and scoring logic, allowing independent testing of scoring and choice validation.