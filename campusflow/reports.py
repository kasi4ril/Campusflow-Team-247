def extract_ticket_number(ticket_id):
    """
    Extract numeric portion from ticket ID (e.g. 'T001', 'T10', 'T2')
    to ensure proper numeric order instead of alphabetical tie-breaking.
    """
    if isinstance(ticket_id, str):
        digits = "".join(ch for ch in ticket_id if ch.isdigit())
        if digits:
            return int(digits)
    return float('inf')


def get_work_queue(tickets):
    """
    Returns a list of ONLY open tickets, sorted by priority (critical > high > medium > low)
    and then by numeric ID for tie-breaking.
    An in_progress or resolved ticket must not appear in this queue.
    """
    # 1. Filter for strictly OPEN tickets only
    open_tickets = [t for t in tickets if t.get("status") == "open"]
            
    # 2. Priority ranking order: lower rank sorts higher
    priority_rank = {
        "critical": 1,
        "high": 2,
        "medium": 3,
        "low": 4
    }
    
    # 3. Sort by priority rank, then by numeric ticket ID for ties
    def sorting_rule(ticket):
        rank = priority_rank.get(str(ticket.get("priority", "")).lower(), 99)
        return (rank, extract_ticket_number(ticket.get("id", "")))
        
    open_tickets.sort(key=sorting_rule)
    return open_tickets


def generate_report(tickets):
    """
    Generates a summary report of all tickets, broken down by status and priority.

    Args:
        tickets (list): The list of all ticket dictionaries.

    Returns:
        dict: A summary containing total count, and breakdowns by status and priority.
    """
    # 1. Set up the empty report template
    report = {
        "total": len(tickets),
        "by_status": {},
        "by_priority": {}
    }
    
    # 2. Loop through every ticket and tally them up
    for ticket in tickets:
        status = ticket.get("status")
        priority = ticket.get("priority")
        
        # Tally the status
        if status:
            if status not in report["by_status"]:
                report["by_status"][status] = 0
            report["by_status"][status] += 1
            
        # Tally the priority
        if priority:
            if priority not in report["by_priority"]:
                report["by_priority"][priority] = 0
            report["by_priority"][priority] += 1
            
    # 3. Return the finished report
    return report