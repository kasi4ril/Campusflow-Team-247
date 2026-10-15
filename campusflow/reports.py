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
    Generates a comprehensive quality summary report of all tickets.

    Metrics include:
    - total: Total number of tickets
    - by_status: Breakdown count by ticket status
    - by_priority: Breakdown count by ticket priority
    - by_category: Breakdown count by ticket category
    - unresolved: Count of tickets in 'open' or 'in_progress' status
    - resolved: Count of tickets in 'resolved' status
    - resolution_percentage: (resolved / total * 100), safely 0.0% for empty datasets
    """
    total = len(tickets)
    by_status = {}
    by_priority = {}
    by_category = {}
    resolved_count = 0
    unresolved_count = 0

    for ticket in tickets:
        status = ticket.get("status")
        priority = ticket.get("priority")
        category = ticket.get("category")

        # Tally status
        if status:
            by_status[status] = by_status.get(status, 0) + 1

        # Tally priority
        if priority:
            by_priority[priority] = by_priority.get(priority, 0) + 1

        # Tally category
        if category:
            by_category[category] = by_category.get(category, 0) + 1

        # Tally resolved vs unresolved
        if status == "resolved":
            resolved_count += 1
        elif status in ["open", "in_progress"]:
            unresolved_count += 1

    resolution_percentage = (resolved_count / total * 100.0) if total > 0 else 0.0

    return {
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_category": by_category,
        "unresolved": unresolved_count,
        "resolved": resolved_count,
        "resolution_percentage": round(resolution_percentage, 2)
    }