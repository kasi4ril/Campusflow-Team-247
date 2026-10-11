def calculate_priority(urgency, affected_users):
    
    """
    calculate_priority(urgency, affected_users):
    
        calculates the urgency of a report and checkes the numbers of affected user.
        
        the condition flow:
            if the urgency of the report is high and the number of affected users  are equal more than ten 'critical'
            if the urgency of the report is high or the number of affected users  are equal more than ten 'high'
            if the urgency of the report is medium and the number of affected users more or equal three 'medium'
            everything else is 'low'
            
               """
    
    urgency_volume = urgency.lower().strip()
    
    try:
        affected_users = int(affected_users)
    except ValueError:
        print("Error: Affected user Must be a whole number")
        return "Expeceted Inputs: (Urgency<str>/Affected User<int>)"
    
    if urgency_volume == "high" and affected_users >= 10:
        priority = "critical"
    elif urgency_volume == "high" or affected_users >= 10:
        priority = "high"
    elif urgency_volume == "medium" or affected_users >= 3:
        priority = "medium"
    else:
        priority = "low"
    return priority



def validate_category(category):
    """
    Validate_category(category):
    
        validate and make sure the user do not use any othere category except the one provided.
    """
    allowed_categories =["network", "hardware", "software", "other"]
    cleaned_category = category.strip().lower()
    if cleaned_category in allowed_categories:
        return True

    return False


def create_ticket(ticket_id, title, category, urgency, affected_users):
    """
    create_ticket(ticket_id, title, category, urgency, affected_users,):
    
        create a dictionary object and store the reports contents and return the object.
            
            """
    if not validate_category(category):
        return "Error: Category not allowed"
    
    ticket = {
    "id": ticket_id,
    "title": title,
    "category":category.strip().title(),
    "urgency": urgency,
    "affected_users": affected_users,
    "priority": calculate_priority(urgency, affected_users),
    "status": "open",
    "assigned_to": None
    }
    print(ticket)  



#for output testing
if __name__ == "__main__":
    new = create_ticket("T001", "HardWare Issuse", "HardWare", "high", 12 )
print(new)
