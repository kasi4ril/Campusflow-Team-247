# CampusFlow Next - Sprint 2 Engineering Reflections

**Team:** CampusFlow Team 247  
**Engineers:** 
- **Engineer A:** Shuaib (Ticket Safety, Centralized Validation & Safe Storage)
- **Engineer B:** Shwarji Khatang (Search, Enhanced Analytics, CLI & Understanding Check)  
**Target Band:** Advanced Engineering Reliability (100/100)

---

## Engineer A: Shuaib

### 1. One Verified Mistake
* **Description:** In the initial v1 prototype, `affected_users` validation allowed boolean values like `True` and `False` to pass because in Python `bool` is a subclass of `int` (`isinstance(True, int)` evaluates to `True`), automatically treating `True` as `1`.
* **Correction:** Implemented strict type inspection (`type(affected_users) is not int or affected_users <= 0`) in `campusflow/validation.py`, rejecting booleans and floats before any mutation occurs (Invariant I3).

### 2. One Key Learning Gain
* **Description:** Mastered safe atomic JSON storage patterns using `tempfile.NamedTemporaryFile` and `os.replace`.
* **Impact:** Prevents partial writes or disk corruption if a save operation fails or terminates unexpectedly mid-stream, ensuring the previous valid JSON database remains 100% intact (Invariant I5).

### 3. One Improvement Received Through Code Review
* **Description:** During reciprocal peer review, Engineer B identified that note ID generation was private inside `add_note` and that `create_ticket` needed to safely accept numeric strings from CLI `input()`.
* **Action Taken:** Extracted `generate_note_id(ticket)` as an exported public API and added numeric string casting in `campusflow/tickets.py`, aligning with contract Section 3.1.

---

## Engineer B: Shwarji Khatang

### 1. One Verified Mistake
* **Description:** When implementing `generate_report`, I initially considered having empty datasets return `None` or an empty string for `resolution_percentage`.
* **Discovery:** During testing, formatting `None` with percentage signs in the CLI triggered a fatal `TypeError: unsupported format string passed to NoneType`.
* **Correction:** Refactored `generate_report` to return well-typed `0.0` as a float when `total == 0`, ensuring clean CLI presentation without division errors.

### 2. One Key Learning Gain
* **Description:** Deepened understanding of caseless Unicode string comparison (`str.casefold()` vs `str.lower()`) and composing multi-filter queries using logical `AND`.
* **Impact:** `.casefold()` provides defensive caseless matching across special characters, and `AND` ensures all active filter criteria narrow search results deterministically without mutating the source list.

### 3. One Improvement Received Through Code Review
* **Description:** Cross-reviewed and integrated Bug-Hunter suites (`BH-1` and `BH-2`) to test partner modules for unlisted edge cases.
* **Action Taken:** Designed `test_bug_hunter_engineer_b_checks_a` to verify that whitespace-padded note messages (e.g. `"   ok   "`) are rejected on stripped length without consuming note IDs or mutating ticket state.
