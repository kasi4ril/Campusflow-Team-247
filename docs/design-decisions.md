# Design Decisions and Function Contracts

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