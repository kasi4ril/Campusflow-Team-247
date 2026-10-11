"""
CampusFlow - Command-Line Helpdesk Ticket Manager
Entry point for the application.
"""
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, update_status
from campusflow.reports import get_work_queue, generate_report

def display_ticket_summary(t):
    """Helper to format a single ticket line."""
    assigned = t.get('assigned_to') or 'Unassigned'
    return f"[{t['id']}] {t['title']} | Priority: {t['priority'].upper()} | Status: {t['status']} | Assigned: {assigned}"

def display_ticket_details(t):
    """Helper to display full ticket details."""
    print(f"\n--- Ticket {t['id']} Details ---")
    print(f"Title:          {t['title']}")
    print(f"Category:       {t['category']}")
    print(f"Urgency:        {t['urgency']}")
    print(f"Affected Users: {t['affected_users']}")
    print(f"Priority:       {t['priority'].upper()}")
    print(f"Status:         {t['status']}")
    print(f"Assigned To:    {t.get('assigned_to') or 'Unassigned'}")

def main():
    print("=" * 45)
    print("      Welcome to CampusFlow Helpdesk")
    print("=" * 45)

    # F7: Load tickets on startup
    try:
        tickets = load_tickets()
        print(f"Loaded {len(tickets)} existing ticket(s) from storage.")
    except Exception as e:
        print(f"Error loading tickets: {e}")
        return

    while True:
        print("\n" + "-" * 30)
        print("          MAIN MENU")
        print("-" * 30)
        print("1. Create Ticket")
        print("2. List All Tickets")
        print("3. View Ticket Details")
        print("4. Assign Ticket")
        print("5. Update Ticket Status")
        print("6. View Work Queue")
        print("7. View Summary Report")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ").strip()

        # F1: Create Ticket
        if choice == '1':
            print("\n--- Create Ticket ---")
            title = input("Enter ticket title: ")
            print("Categories: Network, Hardware, Software, Other")
            category = input("Enter category: ")
            print("Urgency: low, medium, high")
            urgency = input("Enter urgency: ")
            affected_users = input("Enter number of affected users: ")

            try:
                ticket = create_ticket(tickets, title, category, urgency, affected_users)
                save_tickets(tickets)
                print(f"\nSuccess! Ticket created with ID: {ticket['id']} [Priority: {ticket['priority'].upper()}]")
            except Exception as e:
                print(f"Error: {e}")

        # F2: List All Tickets
        elif choice == '2':
            print("\n--- All Tickets ---")
            if not tickets:
                print("No tickets found in the system.")
            else:
                for t in tickets:
                    print(display_ticket_summary(t))

        # F2: View Specific Ticket Details
        elif choice == '3':
            ticket_id = input("\nEnter Ticket ID to view (e.g. T001): ").strip().upper()
            found = next((t for t in tickets if t["id"] == ticket_id), None)
            if found:
                display_ticket_details(found)
            else:
                print(f"Error: Ticket with ID '{ticket_id}' not found.")

        # F3: Assign Ticket
        elif choice == '4':
            ticket_id = input("\nEnter Ticket ID to assign: ").strip().upper()
            staff_name = input("Enter staff member name: ").strip()
            try:
                assign_ticket(tickets, ticket_id, staff_name)
                save_tickets(tickets)
                print(f"Success! Ticket {ticket_id} assigned to '{staff_name}'.")
            except Exception as e:
                print(f"Error: {e}")

        # F4: Update Status
        elif choice == '5':
            ticket_id = input("\nEnter Ticket ID to update: ").strip().upper()
            print("Statuses: open, in_progress, resolved")
            new_status = input("Enter new status: ").strip().lower()
            try:
                update_status(tickets, ticket_id, new_status)
                save_tickets(tickets)
                print(f"Success! Ticket {ticket_id} status updated to '{new_status}'.")
            except Exception as e:
                print(f"Error: {e}")

        # F5: View Work Queue
        elif choice == '6':
            queue = get_work_queue(tickets)
            print("\n--- Active Work Queue (Prioritized) ---")
            if not queue:
                print("No active tickets in queue.")
            else:
                for idx, t in enumerate(queue, 1):
                    assigned = t.get('assigned_to') or 'Unassigned'
                    print(f"{idx}. [{t['priority'].upper()}] {t['id']}: {t['title']} | Assigned: {assigned}")

        # F6: View Reports
        elif choice == '7':
            report = generate_report(tickets)
            print("\n--- Helpdesk Summary Report ---")
            print(f"Total Tickets: {report['total']}")
            print("\nBreakdown by Status:")
            if report['by_status']:
                for status, count in report['by_status'].items():
                    print(f"  • {status}: {count}")
            else:
                print("  (None)")

            print("\nBreakdown by Priority:")
            if report['by_priority']:
                for priority, count in report['by_priority'].items():
                    print(f"  • {priority.upper()}: {count}")
            else:
                print("  (None)")

        # F7: Exit and Save
        elif choice == '8':
            save_tickets(tickets)
            print("\nAll tickets saved to storage. Goodbye!")
            break

        else:
            print("Invalid option. Please choose between 1 and 8.")

if __name__ == "__main__":
    main()