# CampusFlow Next: Engineering Sprint Guide & Technical Contract

**Project:** CampusFlow Next (Sprint 2 Quality, Reliability & Search Upgrade)  
**Target Band:** Advanced Engineering Reliability (100/100)  
**Team:** CampusFlow Team 247  
**Engineers:** 
- **Engineer A (Shuaib):** Ticket Safety, Centralized Validation & Safe Storage
- **Engineer B (Shwarji Khatang):** Search, Enhanced Analytics, CLI Notes UI & Understanding Check  
**Repository:** `https://github.com/kasi4ril/Campusflow-Team-Shwarji-Gabriel.git`

---

## 1. Architectural Boundaries & Non-Negotiable Standards

1. **Pure Python Standard Library Only**:
   - No external packages (no Django, Flask, FastAPI, React, SQL, pandas, pydantic, or pytest).
   - Use built-in modules only: `json`, `os`, `unittest`, `sys`.
2. **Defensive Programming & Validate-Before-Mutate**:
   - Every mutating function must validate ALL inputs **before** modifying the ticket dictionary or ticket list.
   - If validation fails, raise an appropriate exception (`ValueError`, `KeyError`, etc.).
   - **State Invariance:** If an operation fails, the ticket collection and ticket dictionary must remain **100% unchanged** (no partial mutations, no consumed IDs).
3. **Pure Functions vs. CLI Separation**:
   - Business logic in `campusflow/` must NEVER call `input()` or `print()`.
   - All user I/O is handled strictly by `main.py` and `campusflow/understanding_check.py`.
   - Business functions accept parameters and return values or raise exceptions.
4. **Preservation of Baseline Features**:
   - Priority rule precedence must remain identical:
     1. `critical`: `urgency == "high"` AND `affected_users >= 10`
     2. `high`: `urgency == "high"` OR `affected_users >= 10`
     3. `medium`: `urgency == "medium"` OR `affected_users >= 3`
     4. `low`: all other valid tickets.
   - Open Work Queue must contain **strictly `open` tickets** (in_progress and resolved tickets must never appear). Ties must sort by **numeric** ticket ID.

---

## 2. Data Schemas & Invariants

### 2.1 Ticket Schema
```python
{
    "id": "T001",                   # str: T followed by 3+ digits, unique, sequential
    "title": "Wi-Fi router down",   # str: non-blank after .strip()
    "category": "Network",          # str: canonical title-case (Network, Hardware, Software, Other)
    "urgency": "high",              # str: canonical lower-case (low, medium, high)
    "affected_users": 15,           # int: strictly positive int (>= 1). Booleans, floats, strings rejected!
    "priority": "critical",         # str: calculated by precedence rule
    "status": "open",               # str: open, in_progress, resolved
    "assigned_to": "Ada Lovelace",  # str or None (non-empty string required for in_progress)
    "notes": []                     # list: list of Note dictionaries, ordered by note_id
}
```

### 2.2 Follow-up Note Schema
```python
{
    "note_id": "N001",              # str: N followed by 3 digits (N001, N002), sequential PER ticket
    "author": "Grace Hopper",       # str: non-blank after .strip()
    "message": "Rebooted router"    # str: 5 to 300 characters after .strip()
}
```

### 2.3 System Invariants
- **Invariant I1 (Status Transitions):** Legal transitions are:
  - `open` → `in_progress` (REQUIRES non-empty `assigned_to`).
  - `in_progress` → `resolved`.
  - `resolved` → `open` (reopening).
  - Any other transition is illegal and must be rejected.
- **Invariant I2 (Resolved Immutability):** A `resolved` ticket cannot receive notes or assignment updates unless reopened to `open`.
- **Invariant I3 (Boolean Rejection):** In Python, `isinstance(True, int)` evaluates to `True`. The validation helper must explicitly reject `bool` types for `affected_users` (e.g. `if type(affected_users) is bool or not isinstance(affected_users, int): raise ValueError(...)`).
- **Invariant I4 (Note ID Continuity):** A rejected note attempt must NEVER consume or increment the note ID counter.
- **Invariant I5 (Load State Safety):** When loading JSON, if ANY record is corrupt or contains duplicate IDs, the entire load is rejected with a clear exception, and current in-memory tickets remain untouched.

---

## 3. Function Contracts & Shared Interfaces

### 3.1 Validation & Storage (Engineer A Ownership)

```python
# campusflow/validation.py (or tickets.py)
def validate_title(title: str) -> str:
    """Returns trimmed title or raises ValueError if blank."""

def validate_category(category: str) -> str:
    """Returns canonical category ('Network', 'Hardware', 'Software', 'Other') or raises ValueError."""

def validate_urgency(urgency: str) -> str:
    """Returns canonical urgency ('low', 'medium', 'high') or raises ValueError."""

def validate_affected_users(affected_users) -> int:
    """Validates strictly positive integer. Rejects bools, floats, negative/0 values."""

def can_transition(current_status: str, new_status: str, assigned_to: str | None) -> bool:
    """Returns True if transition is valid according to lifecycle rules; otherwise False/raises ValueError."""

# campusflow/notes.py
def generate_note_id(ticket: dict) -> str:
    """Calculates next sequential note ID for the given ticket (e.g. 'N001')."""

def add_note(ticket: dict, author: str, message: str) -> dict:
    """
    Validates ticket status (must be open or in_progress), author, and message (5-300 chars).
    Appends new note to ticket['notes'] and returns the created note dict.
    Raises ValueError on validation failure without modifying ticket['notes'].
    """

# campusflow/storage.py
def validate_ticket_record(ticket: dict, seen_ids: set) -> None:
    """Validates full schema, allowed values, and ID uniqueness of a loaded ticket record."""

def load_tickets(file_path: str = DEFAULT_FILE_PATH) -> list[dict]:
    """
    Safely parses JSON and validates all records BEFORE returning.
    Raises ValueError if corrupted, missing keys, or duplicate IDs found.
    """

def save_tickets(tickets: list[dict], file_path: str = DEFAULT_FILE_PATH) -> None:
    """Creates parent directories if necessary and writes tickets atomically."""
```

### 3.2 Search, Analytics & CLI (Engineer B Ownership)

```python
# campusflow/search.py
def search_tickets(
    tickets: list[dict],
    title: str | None = None,
    category: str | None = None,
    status: str | None = None,
    priority: str | None = None
) -> list[dict]:
    """
    Filters tickets using case-insensitive substring matching (title.casefold())
    and combined logical AND across all provided optional filters.
    Read-only: creates and returns a new list without mutating input tickets.
    """

# campusflow/reports.py
def generate_report(tickets: list[dict]) -> dict:
    """
    Returns dictionary with metrics:
    - total: int
    - by_status: dict (counts per status)
    - by_priority: dict (counts per priority)
    - by_category: dict (counts per category)
    - unresolved: int (open + in_progress)
    - resolved: int
    - resolution_percentage: float (0.0 if total == 0)
    """

# campusflow/understanding_check.py
def run_understanding_check() -> int:
    """
    Runs the 6-question interactive quiz via CLI.
    Validates A/B/C/D input with retry loop.
    Collects explanations for at least 2 questions.
    Returns final score (0-6).
    """
```

---

## 4. Test Lab: 14 Required Scenarios + 2 Bug-Hunter Tests

All tests must pass under `python3 -m unittest discover -s tests -v`.

| Test ID | Test Name | Engineer Owner | Target Scenario |
| :--- | :--- | :--- | :--- |
| **T01** | `test_priority_rules_precedence` | A | Priority precedence matches specification exactly |
| **T02** | `test_unassigned_open_to_in_progress_rejected` | A | Moving unassigned open ticket to in_progress raises ValueError; data unchanged |
| **T03** | `test_resolved_ticket_mutations_rejected` | A | Attempting assignment or status change on resolved ticket raises ValueError |
| **T04** | `test_invalid_affected_users_types` | A | Reject 0, -1, 3.5, "five", and critically `True` / `False` booleans |
| **T05** | `test_add_valid_note` | A | Note added successfully with correct ID (`N001`), preserved in `ticket["notes"]` |
| **T06** | `test_invalid_note_preserves_id_counter` | A | Blank author or message (<5 or >300 chars) rejected; next note still gets `N001` |
| **T07** | `test_note_on_resolved_ticket_lifecycle` | A | Note on resolved ticket rejected; accepted after ticket reopened to open |
| **T08** | `test_search_title_case_insensitive` | B | Substring match on title ignores case (using `.casefold()`) |
| **T09** | `test_combined_search_filters_and_logic` | B | Multi-filter search requires ALL supplied filters to match (logical AND) |
| **T10** | `test_report_zero_tickets_resolution_percentage` | B | Empty ticket list outputs 0.0% resolution rate without ZeroDivisionError |
| **T11** | `test_report_counts_with_fixture` | B | Total, by_status, by_category, resolved, and unresolved match known fixture |
| **T12** | `test_save_load_preserves_notes_and_ids` | A | Persistence roundtrip preserves all notes and next ID generation |
| **T13** | `test_corrupt_or_duplicate_json_rejected` | A | Corrupted JSON or duplicate IDs rejected without altering memory |
| **T14** | `test_understanding_check_scoring` | B | Scoring logic awards 1 point per correct answer and rejects invalid options |
| **BH-1** | `test_bug_hunter_engineer_a_checks_b` | A | Engineer A tests Engineer B's search/report edge case |
| **BH-2** | `test_bug_hunter_engineer_b_checks_a` | B | Engineer B tests Engineer A's validation/storage edge case |

---

## 5. Git Collaboration & Peer Review Protocol

1. **GitHub Issues**:
   - Issue 1: *Engineer A: Centralized validation, notes data model, and safe JSON storage*
   - Issue 2: *Engineer B: Multi-filter search, enhanced analytics, and CLI Understanding Check*
2. **Branching**:
   - Engineer A branch: `feat/validation-and-notes`
   - Engineer B branch: `feat/search-and-insights`
3. **Commit Standards**:
   - Format: `<type>: <concise description>` (`feat:`, `fix:`, `test:`, `docs:`)
   - At least 2 atomic commits per engineer.
4. **Mandatory Reciprocal Code Review**:
   - Engineer A reviews Engineer B's PR; Engineer B reviews Engineer A's PR.
   - **Review standard:** Minimum 2 detailed, actionable comments citing specific files, lines, and edge cases.
   - Strictly forbidden: Rubber-stamping ("LGTM", "Looks good").
   - Reviews must be recorded and feedback addressed before merge into `main`.

---

## 6. AI Learning Log Requirements (`docs/ai-learning-log.md`)

Each engineer must record at least **2 distinct learning cycles** (4 total) adhering to the standard template:
1. **Concept Gap / Problem Statement**
2. **Initial Assumption vs. Question Asked to AI**
3. **AI Guidance Summary**
4. **Independent Mini-Experiment** (isolated script or test run)
5. **Independent Verification Source** (Python docs / unittest failure)
6. **Engineering Decision**
7. **Mandatory Team Rule:** At least ONE cycle across the team must document an AI recommendation that was **tested, found deficient/unsafe, and modified or rejected**.

