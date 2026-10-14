# Baseline Check: CampusFlow Diagnostic

**Date:** 2026-10-14  
**Audited Commit SHA:** `813dd26` (HEAD on `main`)  
**Repository:** `https://github.com/kasi4ril/Campusflow-Team-Shwarji-Gabriel.git`  
**Engineers:** Engineer A (Gabriel), Engineer B (Khatang / Shwarji)

---

## 1. Initial Test Run & Reproduction

### Command Executed:
```bash
python3 -m unittest discover -s tests -v
```

### Initial Results (Audited Commit):
- **Total Tests Run:** 14
- **Passed:** 12
- **Failed / Errored:** 2

#### Error Trace:
```text
======================================================================
ERROR: test_corrupted_json_raises_error (test_storage.TestStorage.test_corrupted_json_raises_error)
----------------------------------------------------------------------
FileNotFoundError: [Errno 2] No such file or directory: 'data/test_tickets.json'

======================================================================
ERROR: test_save_and_load_preserves_data (test_storage.TestStorage.test_save_and_load_preserves_data)
----------------------------------------------------------------------
FileNotFoundError: [Errno 2] No such file or directory: 'data/test_tickets.json'

FAILED (errors=2)
```

### Root Cause Analysis:
The repository did not include the `data/` directory on a fresh clone. `storage.save_tickets` and `tests/test_storage.py` assumed `data/` already existed on the filesystem when calling `open(file_path, "w")`, throwing a fatal `FileNotFoundError`.

### Resolution Applied:
1. Updated `campusflow/storage.py` to ensure `os.makedirs(dir_name, exist_ok=True)` is called if a directory path is supplied.
2. Updated `tests/test_storage.py` `setUp()` to ensure `os.makedirs(os.path.dirname(self.test_file), exist_ok=True)` is called before writing.
3. Added `data/.gitkeep` to track the directory across fresh git clones.
4. Re-ran test discovery: **14/14 tests pass successfully.**

---

## 2. Additional Baseline Audit Findings & Fixes

### Invariant 1: Open Work Queue Scope
- **Audit Observation:** The specification states: *"Original Open Work Queue must show only OPEN tickets... An in_progress or resolved ticket must not appear in this original queue."*
- **Baseline Bug Found:** `campusflow/reports.py` filtered tickets using `if ticket["status"] != "resolved":`, mistakenly including `in_progress` tickets in the open work queue.
- **Resolution Applied:** Refactored filter to strictly `ticket.get("status") == "open"` and updated `tests/test_reports.py` to assert exclusion of `in_progress` tickets.

### Invariant 2: Numeric Ticket ID Tie-Breaking
- **Audit Observation:** When two tickets share the same priority, sorting alphabetically by string ID places `T10` before `T2` because `'1' < '2'`. The specification mandates numeric ticket ID ordering.
- **Baseline Bug Found:** `sorting_rule` used `(rank, ticket["id"])` (lexicographical string comparison).
- **Resolution Applied:** Added `extract_ticket_number` to parse numeric IDs (e.g., `10` vs `2`), ensuring proper numeric tie-breaking order.

---

## 3. Manual Inputs Tested on CLI (`python3 main.py`)

| Input Scenario | Actions / Inputs Provided | Observed Output | Status |
| :--- | :--- | :--- | :--- |
| **Test 1: Valid Ticket Creation** | Choice `1` -> Title: `"Projector flickering in Lab 3"`, Category: `"Hardware"`, Urgency: `"medium"`, Affected: `"4"` | `Success! Ticket created with ID: T001 [Priority: MEDIUM]` | PASS |
| **Test 2: Work Queue Display** | Choice `6` | `1. [MEDIUM] T001: Projector flickering in Lab 3 \| Assigned: Unassigned` | PASS |
| **Test 3: Summary Report Generation** | Choice `7` | Reports total 1, by status (`open: 1`), by priority (`MEDIUM: 1`) | PASS |

---

## 4. Current Status
All baseline defects have been diagnosed, reproduced, and corrected. All 14 original unit tests run and pass without errors. The repository is ready for the CampusFlow Next sprint features (Branches, Issues, Validation, Notes, Multi-Filter Search, and Understanding Check).

