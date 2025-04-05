import mysql.connector
from abc import ABC, abstractmethod
class BookingSystem(ABC):
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ticketbookingsystem"
        )
        self.cursor = self.db.cursor()
        print("✅ Connected to MySQL successfully!")

    @abstractmethod
    def create_event(self, event_name, venue, date, price, total_seats):
        pass

    @abstractmethod
    def book_ticket(self, event_id, num_tickets, customer_id):
        pass

    @abstractmethod
    def cancel_ticket(self, booking_id):
        pass

    @abstractmethod
    def get_available_seats(self, event_id):
        pass

class TicketBookingSystem(BookingSystem):
    def create_event(self, event_name, venue, date, price, total_seats):
        """ Creates an event and stores it in the database """
        try:
            self.cursor.execute("""
                INSERT INTO Event (event_name, venue, event_date, ticket_price, available_seats)
                VALUES (%s, %s, %s, %s, %s)
            """, (event_name, venue, date, price, total_seats))
            self.db.commit()
            print(f"✅ Event '{event_name}' created successfully!")
        except mysql.connector.Error as err:
            print(f"⚠️ Error: {err}")

    def book_ticket(self, event_id, num_tickets, customer_id):
        try:
            self.cursor.execute("SELECT ticket_price, available_seats FROM Event WHERE event_id = %s", (event_id,))
            result = self.cursor.fetchone()

            if not result:
                print("❌ Event not found.")
                return

            ticket_price, available_seats = result
            if num_tickets > available_seats:
                print("❌ Not enough seats available.")
                return

            total_cost = num_tickets * ticket_price

            self.cursor.execute("""
                INSERT INTO Booking (event_id, customer_id, num_tickets, total_cost, booking_date) 
                VALUES (%s, %s, %s, %s, CURDATE())
            """, (event_id, customer_id, num_tickets, total_cost))

            self.cursor.execute("UPDATE Event SET available_seats = available_seats - %s WHERE event_id = %s",
                                (num_tickets, event_id))

            self.db.commit()
            print(f"✅ Successfully booked {num_tickets} tickets for event {event_id}.")

        except mysql.connector.Error as err:
            print(f"⚠️ Error: {err}")

    def cancel_ticket(self, booking_id):
        try:
            self.cursor.execute("SELECT event_id, num_tickets FROM Booking WHERE booking_id = %s", (booking_id,))
            booking = self.cursor.fetchone()

            if not booking:
                print("❌ Booking ID not found.")
                return

            event_id, num_tickets = booking

            self.cursor.execute("DELETE FROM Booking WHERE booking_id = %s", (booking_id,))
            self.cursor.execute("UPDATE Event SET available_seats = available_seats + %s WHERE event_id = %s",
                                (num_tickets, event_id))

            self.db.commit()
            print(f"✅ Booking {booking_id} canceled successfully.")

        except mysql.connector.Error as err:
            print(f"⚠️ Error: {err}")

    def get_available_seats(self, event_id):
        try:
            self.cursor.execute("SELECT available_seats FROM Event WHERE event_id = %s", (event_id,))
            result = self.cursor.fetchone()
            if result:
                print(f"📌 Available seats for event {event_id}: {result[0]}")
            else:
                print("❌ Event not found.")
        except mysql.connector.Error as err:
            print(f"⚠️ Error: {err}")

def main():
    system = TicketBookingSystem()

    while True:
        print("\n🎟️ Ticket Booking System Menu 🎟️")
        print("1. Create Event")
        print("2. Book Tickets")
        print("3. Cancel Tickets")
        print("4. Get Available Seats")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            event_name = input("Enter event name: ")
            venue = input("Enter venue: ")
            date = input("Enter event date (YYYY-MM-DD): ")
            price = float(input("Enter ticket price: "))
            total_seats = int(input("Enter total available seats: "))
            system.create_event(event_name, venue, date, price, total_seats)

        elif choice == "2":
            event_id = int(input("Enter event ID: "))
            num_tickets = int(input("Enter number of tickets: "))
            customer_id = int(input("Enter customer ID: "))
            system.book_ticket(event_id, num_tickets, customer_id)

        elif choice == "3":
            booking_id = int(input("Enter booking ID to cancel: "))
            system.cancel_ticket(booking_id)

        elif choice == "4":
            event_id = int(input("Enter event ID to check available seats: "))
            system.get_available_seats(event_id)

        elif choice == "5":
            print("👋 Exiting the Ticket Booking System. Have a great day!")
            break

        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
