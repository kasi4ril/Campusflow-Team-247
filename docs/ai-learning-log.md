# CampusFlow AI Learning Log: Progressive Journal

This log records verified AI interactions across project sprints, showing how AI suggestions were scrutinized, tested independently, and accepted or rejected based on evidence.

---

# Part 1: Sprint 1 Baseline AI Log (Engineer B: Shwarji Khatang)

### Interaction #1 — Terminal Paths in TDD
**Problem:** `unittest discover` failed to find my test module.
**My initial understanding:** I thought I should run the test command while inside the `tests/` folder.
**Prompt to AI:** Pasted my terminal error: `ImportError: Start directory is not importable`
**Useful AI guidance:** Told me to `cd ..` and run the command from the project root folder.
**My independent experiment/test:** Moved to the root folder and re-ran the test command.
**Verification source or result:** Got the correct `ImportError`, proving the TDD setup worked.
**Decision:** Accepted. Paths matter in Python.
**Related file/commit:** `tests/test_workflow.py`
**What I can now explain without AI:** You must run `unittest discover` from the project root directory so Python can correctly map and import project modules.

---

### Interaction #2 — Dictionary Syntax
**Problem:** I made a syntax error when trying to read a value from a ticket dictionary.
**My initial understanding:** I wrote `ticket("status")`, treating it like a function call.
**Prompt to AI:** "what about now? [pasted code]"
**Useful AI guidance:** Pointed out that `ticket("status")` causes a `TypeError` and must be changed to `ticket["status"]`.
**My independent experiment/test:** Changed parentheses to square brackets and ran tests.
**Verification source or result:** Tests passed (`OK`).
**Decision:** Accepted and fixed code prior to it crashing.
**Related file/commit:** `campusflow/workflow.py`
**What I can now explain without AI:** Dictionaries require square brackets `[]` for key lookups; parentheses `()` are for calling functions.

---

### Interaction #3 — Custom Sorting
**Problem:** I needed to sort tickets by a custom priority (critical → high → medium → low).
**My initial understanding:** I knew `.sort()` existed but didn't know how to rank non-alphabetical strings.
**Prompt to AI:** How do I implement the Work Queue (F5) sorting logic?
**Useful AI guidance:** Suggested mapping strings to numbers (e.g., critical=1, high=2) using a dictionary, and passing that logic to `.sort(key=...)`.
**My independent experiment/test:** Wrote `get_work_queue` using the dictionary mapping trick.
**Verification source or result:** `test_work_queue_sorting` passed successfully.
**Decision:** Accepted. Cleanest way to sort custom data.
**Related file/commit:** `campusflow/reports.py`
**What I can now explain without AI:** How to use a dictionary to map strings to numbers so Python knows how to sort them in custom rank order.

---

# Part 2: Sprint 2 CampusFlow Next AI Log (Team 247)

## Engineer A: Shuaib (Ticket Safety, Validation & Storage)

### Interaction A1 — Validating Booleans in Python Type Hierarchies

**Problem:** Affected-user counts must be positive integers, but Python treats booleans as a subtype of integers.

**My initial understanding:** I understood that zero and negative counts were invalid, but needed to verify how Python handles `True` and `False`.

**Question asked to AI:** How can validation accept positive integers while rejecting booleans, floats, and strings?

**Useful AI guidance:** Use `type(value) is int` when the requirement specifically excludes booleans, and also check that the value is greater than zero.

**My independent experiment/test:** Added invalid values `0`, `-1`, `3.5`, `"five"`, `True`, `False`, and `None` to the ticket validation tests.

**Verification source or result:** Ran `python3 -m unittest discover -s tests -v`. The affected-user validation test passed.

**Decision:** Accepted after testing.

**Related files:** `campusflow/validation.py`, `campusflow/tickets.py`, `tests/test_tickets.py`

**What I can now explain without AI:** Python's `bool` type is a subtype of `int`, so `isinstance(True, int)` is true. An exact type check rejects booleans when only real integers are allowed.

### Interaction A2 — Safe Atomic JSON Validation & State Preservation

**Problem:** Loading a JSON file with corrupt or invalid ticket records must not return partially loaded data. Saving must not replace a valid file with invalid ticket data.

**My initial understanding:** I knew JSON could be loaded and saved, but needed to ensure validation happened before data was accepted or written.

**Question asked to AI:** How can ticket storage reject invalid records and preserve existing data when validation fails?

**Useful AI guidance:** Parse and validate the complete collection before returning it. Validate records before saving, and use a temporary file followed by `os.replace` for atomic replacement.

**My independent experiment/test:** Added tests for corrupt JSON, duplicate ticket IDs, invalid records, invalid status types, and preservation of notes and IDs across save/load.

**Verification source or result:** Ran `python3 -m unittest discover -s tests -v`. The storage tests passed, including the invalid-record and duplicate-ID cases.

**Decision:** Accepted and verified with unit tests.

**Related files:** `campusflow/storage.py`, `tests/test_storage.py`

**What I can now explain without AI:** Validate the complete dataset before accepting it. A temporary file and atomic replacement help prevent a failed save from leaving a partially written destination file.

---

## Engineer B: Shwarji Khatang (Search, Reports & CLI)

### Interaction B1 — Casefold vs Lower for Search Substrings
*(To be completed during implementation)*

### Interaction B2 — Multi-filter AND Logic & Empty Dataset Reporting
*(To be completed during implementation)*


## Team Learning Cycle — AI Suggestion Critically Reviewed

**Concept gap / problem:** We needed a useful BH-1 test for Engineer B's work queue without duplicating existing coverage.

**Initial AI recommendation:** Test numeric ordering of ticket IDs such as `T2` and `T10`.

**Independent check:** Inspected `tests/test_reports.py` and found that `test_work_queue_sorting` already checks numeric ordering using `T002` and `T010`.

**Finding:** The initial suggestion would duplicate an existing test and provide less additional coverage.

**Engineering decision:** Modified the test idea to check that calling `get_work_queue()` does not mutate the original ticket list, while also checking the returned queue's contents.

**Verification:** Added `tests/test_bug_hunter.py` and ran the full suite. All 25 tests passed.

**Lesson:** Inspect existing tests and verify AI recommendations against the actual code before adopting them.
