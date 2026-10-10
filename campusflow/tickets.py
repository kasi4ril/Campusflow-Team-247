def calculate_priority(urgency, affected_users):
    
    """
    calculate_priority(urgency, affected_users):
    
        calculates the urgency of a report and checkes the numbers of affected user.
        
        the condition flow:
            if the urgency of the report is high and the number of affected users  are equal more than ten 'critical'
            if the urgency of the report is high or the number of affected users  are equal more than ten 'high'
            if the urgency of the report is medium and the number of affected users more or equal three 'medium'
            everything else is 'low'
            
            variable:
            priority stores the value of (critical,high,medium,low) at every given condition.  
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

#for testing
if __name__ == "__main__":
    result = calculate_priority("high", 2)
    print(f"Calculated Priority: {result}")
    