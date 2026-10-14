# CampusFlow Helpdesk — Team 247

CampusFlow is an AI-native command-line ticketing and helpdesk system built in Python for managing campus technical support requests (Wi-Fi outages, hardware failures, environment configurations).

## Team 247 Members & Contributions
* **Engineer A (Shuaib):** Ticket creation, category & input validation, priority calculation engine, ticket follow-up notes data model, safe JSON storage persistence, unit tests (`campusflow/tickets.py`, `campusflow/notes.py`, `campusflow/storage.py`, `tests/test_tickets.py`, `tests/test_storage.py`, `tests/test_notes.py`).
* **Engineer B (Shwarji Khatang):** Multi-filter search, assignment, lifecycle workflow, work queue sorting, helpdesk reporting metrics, CLI interface & Engineering Understanding Check, test suites (`campusflow/workflow.py`, `campusflow/reports.py`, `campusflow/search.py`, `campusflow/understanding_check.py`, `main.py`).

## Setup & Requirements
* **Python Version:** Python 3.10+
* **Dependencies:** None (uses standard Python library: `json`, `os`, `unittest`).

### Running the Application
```bash
python3 main.py