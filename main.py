"""
CampusFlow Next - Command-Line Helpdesk Ticket Manager
Main entry point for interactive CLI.
"""

from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, update_status
from campusflow.reports import get_work_queue, generate_report
from campusflow.search import search_tickets
from campusflow.notes import add_note
from campusflow.understanding_check import run_understanding_check

def display_ticket_summary(t):
    """Helper to format a single ticket line."""
    assigned = t.get('assigned_to') or 'Unassigned'
    category = t.get('category', 'Unknown')
    return f"[{t['id']}] {t['title']} | Category: {category} | Priority: {t['priority'].upper()} | Status: {t['status']} | Assigned: {assigned}"

def display_ticket_details(t):
    """Helper to display full ticket details including notes."""
    print(f"\n--- Ticket {t['id']} Details ---")
    print(f"Title:          {t['title']}")
    print(f"Category:       {t['category']}")
    print(f"Urgency:        {t['urgency']}")
    print(f"Affected Users: {t['affected_users']}")
    print(f"Priority:       {t['priority'].upper()}")
    print(f"Status:         {t['status']}")
    print(f"Assigned To:    {t.get('assigned_to') or 'Unassigned'}")
    
    notes = t.get("notes", [])
    print(f"\nFollow-up Notes ({len(notes)}):")
    if not notes:
        print("  (No follow-up notes recorded)")
    else:
        for n in notes:
            print(f"  • [{n['note_id']}] {n['author']}: {n['message']}")

def main():
    print("=" * 50)
    print("      Welcome to CampusFlow Next Helpdesk")
    print("=" * 50)

    try:
        tickets = load_tickets()
        print(f"Loaded {len(tickets)} existing ticket(s) from storage.")
    except Exception as e:
        print(f"Error loading tickets: {e}")
        return

    while True:
        print("\n" + "-" * 38)
        print("              MAIN MENU")
        print("-" * 38)
        print("1. Create Ticket")
        print("2. List All Tickets")
        print("3. View Ticket Details")
        print("4. Assign Ticket")
        print("5. Update Ticket Status")
        print("6. Add Follow-up Note")
        print("7. View Ticket Notes")
        print("8. Search Tickets (Multi-Filter)")
        print("9. View Work Queue")
        print("10. View Summary Report")
        print("11. Engineering Understanding Check")
        print("12. Exit")

        choice = input("\nEnter your choice (1-12): ").strip()

        # 1: Create Ticket
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

        # 2: List All Tickets
        elif choice == '2':
            print("\n--- All Tickets ---")
            if not tickets:
                print("No tickets found in the system.")
            else:
                for t in tickets:
                    print(display_ticket_summary(t))

        # 3: View Ticket Details
        elif choice == '3':
            ticket_id = input("\nEnter Ticket ID to view (e.g. T001): ").strip().upper()
            found = next((t for t in tickets if t["id"] == ticket_id), None)
            if found:
                display_ticket_details(found)
            else:
                print(f"Error: Ticket with ID '{ticket_id}' not found.")

        # 4: Assign Ticket
        elif choice == '4':
            ticket_id = input("\nEnter Ticket ID to assign: ").strip().upper()
            staff_name = input("Enter staff member name: ").strip()
            try:
                assign_ticket(tickets, ticket_id, staff_name)
                save_tickets(tickets)
                print(f"Success! Ticket {ticket_id} assigned to '{staff_name}'.")
            except Exception as e:
                print(f"Error: {e}")

        # 5: Update Status
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

        # 6: Add Follow-up Note
        elif choice == '6':
            print("\n--- Add Follow-up Note ---")
            ticket_id = input("Enter Ticket ID: ").strip().upper()
            found = next((t for t in tickets if t["id"] == ticket_id), None)
            if not found:
                print(f"Error: Ticket with ID '{ticket_id}' not found.")
                continue

            if found.get("status") == "resolved":
                print("Error: Cannot add notes to a resolved ticket. Please reopen the ticket first.")
                continue

            author = input("Enter note author: ").strip()
            message = input("Enter follow-up message (5-300 characters): ").strip()

            try:
                note = add_note(found, author, message)
                save_tickets(tickets)
                print(f"Success! Note {note['note_id']} added to ticket {ticket_id}.")
            except Exception as e:
                print(f"Error: {e}")

        # 7: View Ticket Notes
        elif choice == '7':
            print("\n--- View Ticket Notes ---")
            ticket_id = input("Enter Ticket ID: ").strip().upper()
            found = next((t for t in tickets if t["id"] == ticket_id), None)
            if not found:
                print(f"Error: Ticket with ID '{ticket_id}' not found.")
                continue

            notes = found.get("notes", [])
            print(f"\nNotes for Ticket {ticket_id} ({found['title']}):")
            if not notes:
                print("  (No follow-up notes recorded for this ticket)")
            else:
                for n in notes:
                    print(f"  • [{n['note_id']}] By: {n['author']} | Message: {n['message']}")

        # 8: Search Tickets (Multi-Filter)
        elif choice == '8':
            print("\n--- Search Tickets (Multi-Filter) ---")
            print("Press Enter to skip any filter.")
            title = input("Enter title substring: ").strip()

            # Optional Category filter with validation
            while True:
                cat = input("Enter category (Network, Hardware, Software, Other) [Enter to skip]: ").strip()
                if not cat:
                    cat = None
                    break
                if cat.lower() in ["network", "hardware", "software", "other"]:
                    cat = cat.title()
                    break
                print("Invalid category! Allowed: Network, Hardware, Software, Other.")

            # Optional Status filter with validation
            while True:
                st = input("Enter status (open, in_progress, resolved) [Enter to skip]: ").strip()
                if not st:
                    st = None
                    break
                if st.lower() in ["open", "in_progress", "resolved"]:
                    st = st.lower()
                    break
                print("Invalid status! Allowed: open, in_progress, resolved.")

            # Optional Priority filter with validation
            while True:
                pr = input("Enter priority (low, medium, high, critical) [Enter to skip]: ").strip()
                if not pr:
                    pr = None
                    break
                if pr.lower() in ["low", "medium", "high", "critical"]:
                    pr = pr.lower()
                    break
                print("Invalid priority! Allowed: low, medium, high, critical.")

            sort_choice = input("Sort results by priority and ticket ID? (y/N): ").strip().lower()
            sort_results = (sort_choice == "y")

            results = search_tickets(
                tickets,
                title=title if title else None,
                category=cat,
                status=st,
                priority=pr,
                sort_results=sort_results
            )

            print(f"\nFound {len(results)} matching ticket(s):")
            if not results:
                print("No tickets match the supplied search criteria.")
            else:
                for t in results:
                    print(f"  {display_ticket_summary(t)}")

        # 9: View Work Queue
        elif choice == '9':
            queue = get_work_queue(tickets)
            print("\n--- Active Work Queue (OPEN tickets prioritized) ---")
            if not queue:
                print("No active open tickets in queue.")
            else:
                for idx, t in enumerate(queue, 1):
                    assigned = t.get('assigned_to') or 'Unassigned'
                    print(f"{idx}. [{t['priority'].upper()}] {t['id']}: {t['title']} | Assigned: {assigned}")

        # 10: View Summary Report
        elif choice == '10':
            report = generate_report(tickets)
            print("\n--- Helpdesk Summary & Quality Report ---")
            print(f"Total Tickets:          {report['total']}")
            print(f"Unresolved Tickets:     {report['unresolved']} (open + in_progress)")
            print(f"Resolved Tickets:       {report['resolved']}")
            print(f"Resolution Percentage:  {report['resolution_percentage']}%")

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

            print("\nBreakdown by Category:")
            if report['by_category']:
                for category, count in report['by_category'].items():
                    print(f"  • {category}: {count}")
            else:
                print("  (None)")

        # 11: Engineering Understanding Check
        elif choice == '11':
            try:
                score, _ = run_understanding_check()
                print(f"\nUnderstanding Check recorded. Final Score: {score}/6")
            except Exception as e:
                print(f"Error during Understanding Check: {e}")

        # 12: Exit and Save
        elif choice == '12':
            save_tickets(tickets)
            print("\nAll tickets saved to storage. Goodbye!")
            break

        else:
            print("Invalid option. Please choose between 1 and 12.")

if __name__ == "__main__":
    main()