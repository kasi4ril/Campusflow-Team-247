"""
Workflow Module

This module handles the lifecycle and assignment of tickets for the CampusFlow system.
It enforces strict business rules regarding status changes and staff assignments.
"""

def assign_ticket(tickets, ticket_id, staff_name):
    """
    Assigns a specific ticket to a staff member.

    Args:
        tickets (list): The list of all ticket dictionaries.
        ticket_id (str): The unique identifier of the ticket.
        staff_name (str): The name of the staff member taking the ticket.

    Returns:
        dict: The updated ticket dictionary.

    Raises:
        ValueError: If the staff_name is empty or just whitespace.
        KeyError: If the ticket_id is not found in the list.
    """
    if staff_name.strip() == "":
        raise ValueError("Staff name cannot be empty.")
        
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["assigned_to"] = staff_name
            return ticket
            
    raise KeyError(f"Ticket with ID {ticket_id} not found.")


def update_status(tickets, ticket_id, new_status):
    """
    Updates the status of a ticket while enforcing lifecycle business rules.

    Args:
        tickets (list): The list of all ticket dictionaries.
        ticket_id (str): The unique identifier of the ticket.
        new_status (str): The target status ('open', 'in_progress', or 'resolved').

    Returns:
        dict: The updated ticket dictionary.

    Raises:
        ValueError: If the status is invalid, if modifying a resolved ticket without 
                    reopening, or if starting work on an unassigned ticket.
        KeyError: If the ticket_id is not found in the list.
    """
    if new_status not in ["open", "in_progress", "resolved"]:
        raise ValueError("Invalid status. Must be 'open', 'in_progress', or 'resolved'.")
        
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            
            # Rule: A resolved ticket is locked unless explicitly reopened to 'open'
            if ticket["status"] == "resolved" and new_status != "open":
                raise ValueError("Cannot modify a resolved ticket")
                
            # Rule: A ticket must have an owner before work can begin
            if new_status == "in_progress" and ticket.get("assigned_to") is None:
                raise ValueError("Cannot start work on an unassigned ticket.")
                
            ticket["status"] = new_status
            return ticket
            
    raise KeyError("Ticket not found.")