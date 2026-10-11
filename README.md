# Campusflow-Team-Shwarji-Gabriel
# CampusFlow Helpdesk

CampusFlow is an AI-native command-line ticketing and helpdesk system built in Python for managing campus technical support requests (Wi-Fi outages, hardware failures, environment configurations).

## Team Members & Contributions
* **Engineer A (Gabriel):** Ticket creation, category & input validation, priority calculation engine, ticket unit tests (`campusflow/tickets.py`, `tests/test_tickets.py`).
* **Engineer B (Khatang):** Assignment, lifecycle workflow, work queue sorting, helpdesk reporting metrics, JSON storage persistence, test suites (`campusflow/workflow.py`, `campusflow/reports.py`, `campusflow/storage.py`, `main.py`).

## Setup & Requirements
* **Python Version:** Python 3.10+
* **Dependencies:** None (uses standard Python library: `json`, `os`, `unittest`).

### Running the Application
```bash
python3 main.py