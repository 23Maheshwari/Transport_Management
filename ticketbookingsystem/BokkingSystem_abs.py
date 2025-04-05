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
    def book_ticket(self, event_id, num_tickets, customer_id):
        pass

    @abstractmethod
    def view_bookings(self):
        pass
class TicketBookingSystem(BookingSystem):
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

            # Update event seats
            self.cursor.execute("UPDATE Event SET available_seats = available_seats - %s WHERE event_id = %s",
                                (num_tickets, event_id))

            self.db.commit()
            print("✅ Booking successful!")

        except mysql.connector.Error as err:
            print(f"⚠️ Error: {err}")

    def view_bookings(self):
        self.cursor.execute("""
            SELECT b.booking_id, b.num_tickets, e.event_name, c.customer_name, b.total_cost, b.booking_date 
            FROM Booking b
            JOIN Event e ON b.event_id = e.event_id
            JOIN Customer c ON b.customer_id = c.customer_id
        """)
        bookings = self.cursor.fetchall()

        print("\n📌 Current Bookings:")
        for booking in bookings:
            print(
                f"🆔 Booking {booking[0]}: {booking[1]} tickets for {booking[2]} by {booking[3]} - ₹{booking[4]} on {booking[5]}")
if __name__ == "__main__":
    system = TicketBookingSystem()
    system.view_bookings()
    system.book_ticket(1, 3, 2)
