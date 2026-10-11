# AI Learning Log

## Fellow: Khatang (Engineer B)

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