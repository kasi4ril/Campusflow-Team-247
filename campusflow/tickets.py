"""
Tickets Module

Handles ticket creation, input validation, and priority calculation.
"""

from campusflow.validation import (
    validate_title,
    validate_category as validate_category_value,
    validate_urgency,
    validate_affected_users,
)


def calculate_priority(urgency, affected_users):
    """Calculate priority using the required precedence rules."""
    urgency = validate_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def validate_category(category):
    """Preserve the existing boolean validation interface."""
    try:
        validate_category_value(category)
        return True
    except ValueError:
        return False


def generate_ticket_id(tickets):
    """Generate the next sequential ticket ID, such as T001."""
    max_num = 0

    for ticket in tickets:
        ticket_id = ticket.get("id", "")
        if (
            isinstance(ticket_id, str)
            and ticket_id.startswith("T")
            and ticket_id[1:].isdigit()
        ):
            max_num = max(max_num, int(ticket_id[1:]))

    return f"T{max_num + 1:03d}"


def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate all inputs before adding a ticket."""
    title = validate_title(title)
    category = validate_category_value(category)
    urgency = validate_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    priority = calculate_priority(urgency, affected_users)
    ticket_id = generate_ticket_id(tickets)

    new_ticket = {
        "id": ticket_id,
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }

    tickets.append(new_ticket)
    return new_ticket
