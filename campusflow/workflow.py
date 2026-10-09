def assign_ticket(tickets, ticket_id, staff_name):
    if staff_name.strip() == "":
        raise ValueError("Staff name cannot be empty.")
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["assigned_to"] = staff_name
            return ticket
    raise ValueError("Ticket not found.")