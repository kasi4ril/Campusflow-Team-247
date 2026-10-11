"""
Tickets Module

Handles ticket creation, input validation, and priority calculation.
"""

def calculate_priority(urgency, affected_users):
    """
    Calculates ticket priority based on urgency and affected user count.
    
    Order of precedence:
    1. high urgency AND >= 10 affected users -> critical
    2. high urgency OR >= 10 affected users  -> high
    3. medium urgency OR >= 3 affected users -> medium
    4. all remaining valid tickets           -> low
    """
    urgency_volume = urgency.lower().strip()
    if urgency_volume not in ["low", "medium", "high"]:
        raise ValueError("Urgency must be 'low', 'medium', or 'high'.")

    try:
        affected_users = int(affected_users)
    except (ValueError, TypeError):
        raise ValueError("Affected users must be a whole integer.")

    if affected_users <= 0:
        raise ValueError("Affected users must be a positive integer greater than zero.")

    if urgency_volume == "high" and affected_users >= 10:
        return "critical"
    elif urgency_volume == "high" or affected_users >= 10:
        return "high"
    elif urgency_volume == "medium" or affected_users >= 3:
        return "medium"
    else:
        return "low"


def validate_category(category):
    """Validates category against allowed list."""
    allowed = ["network", "hardware", "software", "other"]
    return category.strip().lower() in allowed


def generate_ticket_id(tickets):
    """Generates the next sequential unique ticket ID (e.g. T001, T002)."""
    if not tickets:
        return "T001"
    
    # Extract numbers from IDs like 'T001' -> 1
    max_num = 0
    for t in tickets:
        t_id = t.get("id", "")
        if t_id.startswith("T") and t_id[1:].isdigit():
            max_num = max(max_num, int(t_id[1:]))
            
    return f"T{max_num + 1:03d}"


def create_ticket(tickets, title, category, urgency, affected_users):
    """
    Validates inputs, calculates priority, and appends a new ticket.
    """
    if not title or not title.strip():
        raise ValueError("Title must not be blank.")

    if not validate_category(category):
        raise ValueError(f"Category '{category}' is invalid. Allowed: Network, Hardware, Software, Other.")

    priority = calculate_priority(urgency, affected_users)
    ticket_id = generate_ticket_id(tickets)

    new_ticket = {
        "id": ticket_id,
        "title": title.strip(),
        "category": category.strip().title(),
        "urgency": urgency.strip().lower(),
        "affected_users": int(affected_users),
        "priority": priority,
        "status": "open",
        "assigned_to": None
    }
    
    tickets.append(new_ticket)
    return new_ticket