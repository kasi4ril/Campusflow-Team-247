"""
Search and Multi-Filter Module for CampusFlow Next (Engineer B).

Provides read-only searching and combined filtering for tickets.
Enforces case-insensitive substring matching on titles using .casefold()
and combines category, status, and priority filters using logical AND.
"""

from campusflow.reports import extract_ticket_number

PRIORITY_RANK = {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 4
}

def search_tickets(
    tickets,
    title=None,
    category=None,
    status=None,
    priority=None,
    sort_results=False
):
    """
    Searches and filters tickets based on title substring and optional criteria.

    Args:
        tickets (list): List of ticket dictionaries.
        title (str, optional): Substring to match in ticket title (case-insensitive).
        category (str, optional): Category to match ('Network', 'Hardware', etc.).
        status (str, optional): Status to match ('open', 'in_progress', 'resolved').
        priority (str, optional): Priority to match ('low', 'medium', 'high', 'critical').
        sort_results (bool, optional): If True, sorts results by priority then numeric ID.

    Returns:
        list: A new list containing tickets that match ALL supplied filters.
              Original ticket records and list are never modified.
    """
    # Normalize title query
    title_query = title.strip().casefold() if (title and isinstance(title, str) and title.strip()) else None

    # Normalize category filter
    cat_query = category.strip().casefold() if (category and isinstance(category, str) and category.strip()) else None

    # Normalize status filter
    status_query = status.strip().casefold() if (status and isinstance(status, str) and status.strip()) else None

    # Normalize priority filter
    priority_query = priority.strip().casefold() if (priority and isinstance(priority, str) and priority.strip()) else None

    matches = []

    for ticket in tickets:
        # Title filter: case-insensitive substring match
        if title_query is not None:
            ticket_title = str(ticket.get("title", "")).casefold()
            if title_query not in ticket_title:
                continue

        # Category filter: exact match (case-insensitive)
        if cat_query is not None:
            ticket_cat = str(ticket.get("category", "")).casefold()
            if ticket_cat != cat_query:
                continue

        # Status filter: exact match (case-insensitive)
        if status_query is not None:
            ticket_status = str(ticket.get("status", "")).casefold()
            if ticket_status != status_query:
                continue

        # Priority filter: exact match (case-insensitive)
        if priority_query is not None:
            ticket_priority = str(ticket.get("priority", "")).casefold()
            if ticket_priority != priority_query:
                continue

        # All supplied filters matched (logical AND)
        matches.append(ticket)

    # Optional sorting by priority and numeric ticket ID
    if sort_results:
        def sort_key(t):
            rank = PRIORITY_RANK.get(str(t.get("priority", "")).lower(), 99)
            num_id = extract_ticket_number(t.get("id", ""))
            return (rank, num_id)

        # Return a sorted copy to maintain purity
        return sorted(matches, key=sort_key)

    return list(matches)

