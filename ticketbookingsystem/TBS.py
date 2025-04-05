import mysql.connector

class TicketBookingSystem:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ticketbookingsystem"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def create_event(self):
        event_name = input("Event Name: ").strip()
        event_date = input("Event Date (YYYY-MM-DD): ").strip()
        event_time = input("Event Time (HH:MM:SS): ").strip()
        total_seats = int(input("Total Seats: ").strip())
        ticket_price = float(input("Ticket Price: ").strip())
        event_type = input("Event Type (Movie/Sports/Concert): ").strip()
        venue_name = input("Venue Name: ").strip()
        venue_address = input("Venue Address: ").strip()

        self.cursor.execute("SELECT venue_id FROM venue WHERE venue_name = %s", (venue_name,))
        venue = self.cursor.fetchone()

        if not venue:
            self.cursor.execute("INSERT INTO venue (venue_name, address) VALUES (%s, %s)", (venue_name, venue_address))
            self.conn.commit()
            venue_id = self.cursor.lastrowid
        else:
            venue_id = venue["venue_id"]

        query = """
            INSERT INTO event (event_name, event_date, event_time, venue_id, total_seats, available_seats, ticket_price, event_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (event_name, event_date, event_time, venue_id, total_seats, total_seats, ticket_price, event_type)
        self.cursor.execute(query, values)
        self.conn.commit()

        print(f"✅ Event '{event_name}' added successfully!")

    def view_event_details(self, event_id):
        query = """
            SELECT e.event_name, e.event_date, e.event_time, e.total_seats, e.available_seats, e.ticket_price, e.event_type, 
                   v.venue_name, v.address 
            FROM event e 
            JOIN venue v ON e.venue_id = v.venue_id 
            WHERE e.event_id = %s
        """
        self.cursor.execute(query, (event_id,))
        event = self.cursor.fetchone()

        if not event:
            print("❌ Event not found.")
            return

        print(f"\n📅 Event: {event['event_name']} ({event['event_type']})")
        print(f"📆 Date: {event['event_date']}, ⏰ Time: {event['event_time']}")
        print(f"🎟️ Tickets Available: {event['available_seats']}/{event['total_seats']}, 💰 Price: ₹{event['ticket_price']:.2f}")
        print(f"🏟️ Venue: {event['venue_name']} ({event['address']})")

    def book_tickets(self):
        event_id = input("Enter Event ID: ").strip()
        num_tickets = int(input("Enter number of tickets: ").strip())

        self.cursor.execute("SELECT available_seats, ticket_price FROM event WHERE event_id = %s", (event_id,))
        result = self.cursor.fetchone()

        if not result:
            print("❌ Event not found.")
            return

        available_seats, ticket_price = result["available_seats"], result["ticket_price"]

        if num_tickets > available_seats:
            print(f"❌ Not enough seats available! Only {available_seats} left.")
            return

        total_price = num_tickets * ticket_price
        print(f"💵 Total Price: ₹{total_price:.2f}")

        confirm = input("Confirm booking? (yes/no): ").strip().lower()
        if confirm == "yes":
            new_available_seats = available_seats - num_tickets
            self.cursor.execute("UPDATE event SET available_seats = %s WHERE event_id = %s", (new_available_seats, event_id))
            self.conn.commit()
            print("✅ Booking successful! Enjoy your event 🎉")
        else:
            print("❌ Booking cancelled.")

    def cancel_tickets(self):
        event_id = input("Enter Event ID: ").strip()
        num_tickets = int(input("Enter number of tickets to cancel: ").strip())

        self.cursor.execute("SELECT total_seats, available_seats FROM event WHERE event_id = %s", (event_id,))
        result = self.cursor.fetchone()

        if not result:
            print("❌ Event not found.")
            return

        total_seats, available_seats = result["total_seats"], result["available_seats"]
        new_available_seats = min(total_seats, available_seats + num_tickets)

        self.cursor.execute("UPDATE event SET available_seats = %s WHERE event_id = %s", (new_available_seats, event_id))
        self.conn.commit()
        print(f"✅ {num_tickets} ticket(s) cancelled successfully!")

    def main(self):
        while True:
            print("\n🎟️ Ticket Booking System 🎟️")
            print("1. Create Event")
            print("2. View Event Details")
            print("3. Book Tickets")
            print("4. Cancel Tickets")
            print("5. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.create_event()
            elif choice == "2":
                event_id = input("Enter Event ID: ").strip()
                self.view_event_details(event_id)
            elif choice == "3":
                self.book_tickets()
            elif choice == "4":
                self.cancel_tickets()
            elif choice == "5":
                print("Exiting Ticket Booking System... 👋")
                break
            else:
                print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    system = TicketBookingSystem()
    system.main()
