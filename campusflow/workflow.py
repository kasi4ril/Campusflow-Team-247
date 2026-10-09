def assign_ticket(tickets, ticket_id, staff_name):
    if staff_name.strip() == "":
        raise ValueError("Staff name cannot be empty.")
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["assigned_to"] = staff_name
            return ticket
    raise ValueError("Ticket not found.")

def update_status(tickets, ticket_id, new_status):
    if new_status not in ["open", "in_progress", "resolved"]:
        raise ValueError("Invalid status. Must be 'open', 'in_progress', or 'resolved'.")
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            if ticket["status"] == "resolved" and new_status != "open":
                raise ValueError("Cannot modify a resolved ticket")
            if new_status == "in_progress" and ticket.get("assigned_to") is None:
                raise ValueError("Cannot start work on an unassigned ticket.")
            ticket["status"] = new_status

            return ticket
    raise ValueError("Ticket not found.")