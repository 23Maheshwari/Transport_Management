import mysql.connector
from abc import ABC, abstractmethod

# -------- DB Connection --------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  # Change your DB password
        database="ticketbookingsystem"
    )

# -------- Bean Classes --------
class Venue:
    def __init__(self, name, address):
        self.name = name
        self.address = address

class Event:
    def __init__(self, name, date, time, total_seats, ticket_price, venue):
        self.name = name
        self.date = date
        self.time = time
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.ticket_price = ticket_price
        self.venue = venue

class Movie(Event): pass
class Sports(Event): pass
class Concert(Event): pass

class Customer:
    def __init__(self, name):
        self.name = name

class Booking:
    def __init__(self, event, customers):
        self.event = event
        self.customers = customers
        self.num_tickets = len(customers)
        self.total_cost = 0

    def calculate_booking_cost(self):
        self.total_cost = self.num_tickets * self.event.ticket_price

# -------- Abstract Interface --------
class IBookingSystemRepository(ABC):
    @abstractmethod
    def create_event(self, event_name, date, time, total_seats, ticket_price, event_type, venue): pass

    @abstractmethod
    def get_event_details(self): pass

    @abstractmethod
    def get_available_no_of_tickets(self, event_name): pass

    @abstractmethod
    def book_tickets(self, event_name, num_tickets, list_of_customers): pass

    @abstractmethod
    def cancel_booking(self, booking_id): pass

    @abstractmethod
    def get_booking_details(self, booking_id): pass

# -------- Repository Implementation --------
class BookingSystemRepositoryImpl(IBookingSystemRepository):
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    def create_event(self, event_name, date, time, total_seats, ticket_price, event_type, venue):
        # Check if the venue already exists
        self.cursor.execute("SELECT id FROM venue WHERE name = %s", (venue.name,))
        venue_row = self.cursor.fetchone()

        if venue_row:
            venue_id = venue_row[0]  # Existing venue
        else:
            # Insert new venue
            self.cursor.execute("INSERT INTO venue (name, address) VALUES (%s, %s)", (venue.name, venue.address))
            self.conn.commit()
            venue_id = self.cursor.lastrowid  # Get the new venue_id

        # Determine event type
        if event_type.lower() == "movie":
            event = Movie(event_name, date, time, total_seats, ticket_price, venue)
        elif event_type.lower() == "sports":
            event = Sports(event_name, date, time, total_seats, ticket_price, venue)
        elif event_type.lower() == "concert":
            event = Concert(event_name, date, time, total_seats, ticket_price, venue)
        else:
            raise ValueError("Invalid event type")

        # Insert event
        self.cursor.execute("""
            INSERT INTO event (name, date, time, total_seats, available_seats, ticket_price, type, venue_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (event.name, event.date, event.time, event.total_seats, event.total_seats, event.ticket_price, event_type, venue_id))
        self.conn.commit()
        print("✅ Event Created!")

    def get_event_details(self):
        self.cursor.execute("SELECT * FROM event")
        return self.cursor.fetchall()

    def get_available_no_of_tickets(self, event_name):
        self.cursor.execute("SELECT available_seats FROM event WHERE name = %s", (event_name,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def book_tickets(self, event_name, num_tickets, list_of_customers):
        self.cursor.execute("SELECT id, ticket_price, available_seats FROM event WHERE name = %s", (event_name,))
        event_data = self.cursor.fetchone()
        if not event_data:
            raise ValueError("Event not found")

        event_id, ticket_price, available_seats = event_data
        if available_seats < num_tickets:
            raise ValueError("Not enough seats available")

        total_cost = num_tickets * ticket_price

        # Insert booking first
        self.cursor.execute("INSERT INTO booking (event_id, num_tickets, total_cost) VALUES (%s, %s, %s)",
                            (event_id, num_tickets, total_cost))
        booking_id = self.cursor.lastrowid

        # Insert customers after getting booking ID
        for cust in list_of_customers:
            self.cursor.execute("INSERT INTO customer (name, booking_id) VALUES (%s, %s)",
                                (cust.name, booking_id))

        # Update available seats
        self.cursor.execute("UPDATE event SET available_seats = available_seats - %s WHERE id = %s",
                            (num_tickets, event_id))

        self.conn.commit()
        print(f"✅ Booking successful! Booking ID: {booking_id}, Total Cost: {total_cost}")

    def cancel_booking(self, booking_id):
        self.cursor.execute("SELECT event_id, num_tickets FROM booking WHERE id = %s", (booking_id,))
        result = self.cursor.fetchone()
        if not result:
            raise ValueError("Booking not found")

        event_id, num_tickets = result

        self.cursor.execute("DELETE FROM customer WHERE booking_id = %s", (booking_id,))
        self.cursor.execute("DELETE FROM booking WHERE id = %s", (booking_id,))
        self.cursor.execute("UPDATE event SET available_seats = available_seats + %s WHERE id = %s",
                            (num_tickets, event_id))

        self.conn.commit()
        print("✅ Booking cancelled successfully.")

    def get_booking_details(self, booking_id):
        self.cursor.execute("""
            SELECT e.name, b.num_tickets, b.total_cost
            FROM booking b
            JOIN event e ON b.event_id = e.id
            WHERE b.id = %s
        """, (booking_id,))
        return self.cursor.fetchone()

# -------- Main UI --------
def main():
    repo = BookingSystemRepositoryImpl()

    while True:
        print("\n1. Create Event\n2. Book Tickets\n3. Cancel Tickets\n4. Get Available Seats\n5. Get Event Details\n6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Event Name: ")
            date = input("Date (YYYY-MM-DD): ")
            time = input("Time (HH:MM:SS): ")
            total_seats = int(input("Total Seats: "))
            ticket_price = float(input("Ticket Price: "))
            event_type = input("Type (Movie/Sports/Concert): ")
            vname = input("Venue Name: ")
            vaddress = input("Venue Address: ")
            venue = Venue(vname, vaddress)
            repo.create_event(name, date, time, total_seats, ticket_price, event_type, venue)

        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid Choice!")

if __name__ == "__main__":
    main()
