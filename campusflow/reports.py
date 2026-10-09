def get_work_queue(tickets):
    """
    Returns a list of unresolved tickets, sorted by priority and then by ID.
    """
    # 1. Create a new list with ONLY unresolved tickets
    open_tickets = []
    for ticket in tickets:
        if ticket["status"] != "resolved":
            open_tickets.append(ticket)
            
    # 2. Teach Python the ranking order of priorities
    # Lower numbers will sort to the top of the list
    priority_rank = {
        "critical": 1,
        "high": 2,
        "medium": 3,
        "low": 4
    }
    
    # 3. Sort the list using a custom rule (a lambda function)
    # The rule says: "First sort by the priority number. If they are tied, 
    # sort alphabetically by the ticket 'id' (so T001 comes before T002)."
    def sorting_rule(ticket):
        # Look up the number for the priority. Default to 99 if it's unknown.
        rank = priority_rank.get(ticket["priority"], 99)
        return (rank, ticket["id"])
        
    open_tickets.sort(key=sorting_rule)
    
    # 4. Return the sorted list
    return open_tickets