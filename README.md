# CampusFlow Helpdesk

CampusFlow is an evolving, reliable command-line ticketing and helpdesk system built in Python for managing campus technical support requests (Wi-Fi outages, hardware failures, environment configurations).

---

## Project Progression & History

This codebase follows an iterative, progressive engineering model where each sprint builds upon and hardens previous work rather than discarding it.

### Sprint 1: Baseline Prototype (CampusFlow v1.0)
* **Status:** Progressing Audit Band (70–84/100)
* **Team Members & Core Contributions:**
  * **Engineer A (Gabriel):** Initial ticket creation, category validation, priority rule engine, ticket unit tests (`campusflow/tickets.py`, `tests/test_tickets.py`).
  * **Engineer B (Shwarji Khatang):** Ticket assignment, initial status lifecycle, work queue sorting, initial reporting metrics, baseline JSON persistence (`campusflow/workflow.py`, `campusflow/reports.py`, `campusflow/storage.py`, `main.py`).

### Sprint 2: Reliability, Search & Quality Sprint (CampusFlow Next v2.0)
* **Status:** Completed — Target Band: Advanced Engineering Reliability (100/100)
* **Team:** CampusFlow Team 247
* **Team Members & Upgrades:**
  * **Engineer A (Shuaib):** Centralized defensive validation (`campusflow/validation.py`), boolean-type safety, follow-up notes data model (`campusflow/notes.py`), safe atomic JSON parsing & ID continuity (`campusflow/storage.py`), and corresponding unit test suites.
  * **Engineer B (Shwarji Khatang):** Multi-filter search engine with `.casefold()` and `AND` logic (`campusflow/search.py`), enhanced quality analytics and resolution metrics (`campusflow/reports.py`), interactive CLI notes UI, and the 6-question Engineering Understanding Check (`campusflow/understanding_check.py`).

---

## Setup & Requirements
* **Python Version:** Python 3.10+
* **Dependencies:** None (uses standard Python library only: `json`, `os`, `unittest`, `sys`).

### Running the Application
```bash
python3 main.py
```

### Running the Test Suite
```bash
python3 -m unittest discover -s tests -v
```

---

## Data Schema & Storage Architecture

Data is persisted to disk at `data/tickets.json` as a top-level JSON array of ticket records. Writes are performed atomically using `tempfile` and `os.replace` to prevent partial file corruption.

### Ticket Schema
```json
{
    "id": "T001",
    "title": "Wi-Fi router offline in Library",
    "category": "Network",
    "urgency": "high",
    "affected_users": 15,
    "priority": "critical",
    "status": "open",
    "assigned_to": null,
    "notes": [
        {
            "note_id": "N001",
            "author": "Grace Hopper",
            "message": "Power cycled core router and verified link lights."
        }
    ]
}
```

---

## Key Documentation & Audit Artifacts
* **[Baseline Diagnostic (`docs/baseline-check.md`)](docs/baseline-check.md):** Audit reproduction, test failures, and baseline fixes.
* **[Sprint 2 Engineering Guide (`docs/campusflow-next-sprint-guide.md`)](docs/campusflow-next-sprint-guide.md):** Architecture, function contracts, test matrix, and peer review standards.
* **[Design Decisions (`docs/design-decisions.md`)](docs/design-decisions.md):** Architectural rationale across sprints.
* **[AI Learning Log (`docs/ai-learning-log.md`)](docs/ai-learning-log.md):** Documented concept gaps, experiments, and verified decisions.
* **[Sprint 2 Reflections (`docs/sprint2-reflections.md`)](docs/sprint2-reflections.md):** Verified mistakes, learning gains, and review outcomes.