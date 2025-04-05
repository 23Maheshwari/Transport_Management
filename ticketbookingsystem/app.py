import mysql.connector
from datetime import datetime
from abc import ABC, abstractmethod

# DBUtil.py
def getDBConn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ticketbookingsystem"
    )

# bean/Venue.py
class Venue:
    def __init__(self, name, address):
        self.name = name
        self.address = address

# bean/Event.py
class Event:
    def __init__(self, name, date, time, total_seats, ticket_price, event_type, venue):
        self.name = name
        self.date = date
        self.time = time
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.ticket_price = ticket_price
        self.event_type = event_type
        self.venue = venue

# bean/Customer.py
class Customer:
    def __init__(self, name, email=None, phone=None):
        self.name = name
        self.email = email
        self.phone = phone

# service/IEventServiceProvider.py
class IEventServiceProvider(ABC):
    @abstractmethod
    def create_event(self, event_name, date, time, total_seats, ticket_price, event_type, venue):
        pass

# service/IBookingSystemServiceProvider.py
class IBookingSystemServiceProvider(IEventServiceProvider, ABC):
    @abstractmethod
    def book_tickets(self, event_name, num_tickets, customers):
        pass

    @abstractmethod
    def cancel_booking(self, booking_id):
        pass

    @abstractmethod
    def get_available_seats(self, event_name):
        pass

    @abstractmethod
    def get_event_details(self, event_name):
        pass

    @abstractmethod
    def get_booking_details(self, booking_id):
        pass

# service/IBookingSystemRepository.py
class IBookingSystemRepository(ABC):
    @abstractmethod
    def create_event(self, event_name, date, time, total_seats, ticket_price, event_type, venue):
        pass

    @abstractmethod
    def get_event_details(self, event_name):
        pass

    @abstractmethod
    def get_available_seats(self, event_name):
        pass

    @abstractmethod
    def calculate_booking_cost(self, num_tickets, ticket_price):
        pass

    @abstractmethod
    def book_tickets(self, event_name, num_tickets, customers):
        pass

    @abstractmethod
    def cancel_booking(self, booking_id):
        pass

    @abstractmethod
    def get_booking_details(self, booking_id):
        pass

# bean/BookingSystemRepositoryImpl.py
class BookingSystemRepositoryImpl(IBookingSystemRepository):
    def __init__(self):
        self.connection = getDBConn()
        self.cursor = self.connection.cursor()

    def clear_unread_results(self):
        while self.cursor.nextset():
            pass

    def create_event(self, event_name, date, time, total_seats, ticket_price, event_type, venue):
        self.cursor.execute("SELECT venue_id FROM venue WHERE venue_name = %s AND address = %s", (venue.name, venue.address))
        venue_result = self.cursor.fetchone()

        if venue_result:
            venue_id = venue_result[0]
        else:
            self.cursor.execute("INSERT INTO venue (venue_name, address) VALUES (%s, %s)", (venue.name, venue.address))
            self.connection.commit()
            venue_id = self.cursor.lastrowid

        self.cursor.execute("""
            INSERT INTO event (event_name, event_date, event_time, total_seats, available_seats, ticket_price, event_type, venue_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (event_name, date, time, total_seats, total_seats, ticket_price, event_type, venue_id))
        self.connection.commit()
        print("✅ Event created successfully!")

    def book_tickets(self, event_name, num_tickets, customers):
        self.clear_unread_results()
        self.cursor.execute("SELECT event_id, ticket_price, available_seats FROM event WHERE event_name = %s", (event_name,))
        event = self.cursor.fetchone()

        if not event:
            print("❌ Event not found.")
            return

        event_id, ticket_price, available_seats = event

        if num_tickets > available_seats:
            print("❌ Not enough available seats.")
            return

        for customer in customers:
            self.cursor.execute("INSERT INTO customer (customer_name, email, phone_number) VALUES (%s, %s, %s)",
                                (customer.name, customer.email, customer.phone))
            customer_id = self.cursor.lastrowid

            total_cost = self.calculate_booking_cost(1, ticket_price)
            booking_date = datetime.today().strftime('%Y-%m-%d')

            self.cursor.execute("""
                INSERT INTO booking (num_tickets, total_cost, booking_date, customer_id, event_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (1, total_cost, booking_date, customer_id, event_id))

        self.cursor.execute("UPDATE event SET available_seats = available_seats - %s WHERE event_id = %s",
                            (num_tickets, event_id))
        self.connection.commit()
        print("✅ Tickets booked successfully!")

    def calculate_booking_cost(self, num_tickets, ticket_price):
        return num_tickets * ticket_price

    def cancel_booking(self, booking_id):
        self.cursor.execute("SELECT event_id, num_tickets FROM booking WHERE booking_id = %s", (booking_id,))
        booking = self.cursor.fetchone()

        if not booking:
            print("❌ Booking not found.")
            return

        event_id, num_tickets = booking
        self.cursor.execute("DELETE FROM booking WHERE booking_id = %s", (booking_id,))
        self.cursor.execute("UPDATE event SET available_seats = available_seats + %s WHERE event_id = %s", (num_tickets, event_id))
        self.connection.commit()
        print("✅ Booking cancelled successfully!")

    def get_available_seats(self, event_name):
        self.cursor.execute("SELECT available_seats FROM event WHERE event_name = %s", (event_name,))
        result = self.cursor.fetchone()
        if result:
            print(f"🎟 Available seats for '{event_name}': {result[0]}")
        else:
            print("❌ Event not found.")

    def get_event_details(self, event_name):
        self.cursor.execute("""
            SELECT e.event_name, e.event_date, e.event_time, e.total_seats, e.available_seats,
                   e.ticket_price, e.event_type, v.venue_name, v.address
            FROM event e
            JOIN venue v ON e.venue_id = v.venue_id
            WHERE e.event_name = %s
        """, (event_name,))
        event = self.cursor.fetchone()
        if event:
            print("\n📌 Event Details:")
            print(f"Name: {event[0]}")
            print(f"Date: {event[1]}")
            print(f"Time: {event[2]}")
            print(f"Total Seats: {event[3]}")
            print(f"Available Seats: {event[4]}")
            print(f"Ticket Price: ₹{event[5]}")
            print(f"Type: {event[6]}")
            print(f"Venue: {event[7]}, {event[8]}\n")
        else:
            print("❌ Event not found.")

    def get_booking_details(self, booking_id):
        self.cursor.execute("""
            SELECT b.booking_id, b.num_tickets, b.total_cost, b.booking_date,
                   c.customer_name, c.email, c.phone_number,
                   e.event_name, e.event_date, e.event_time
            FROM booking b
            JOIN customer c ON b.customer_id = c.customer_id
            JOIN event e ON b.event_id = e.event_id
            WHERE b.booking_id = %s
        """, (booking_id,))
        booking = self.cursor.fetchone()
        if booking:
            print("\n📃 Booking Details:")
            print(f"Booking ID: {booking[0]}")
            print(f"Customer: {booking[4]} | Email: {booking[5]} | Phone: {booking[6]}")
            print(f"Event: {booking[7]} on {booking[8]} at {booking[9]}")
            print(f"Tickets Booked: {booking[1]}")
            print(f"Total Cost: ₹{booking[2]}")
            print(f"Booking Date: {booking[3]}\n")
        else:
            print("❌ Booking not found.")

# service/BookingSystemServiceImpl.py
class BookingSystemServiceImpl(IBookingSystemServiceProvider):
    def __init__(self):
        self.repo = BookingSystemRepositoryImpl()

    def create_event(self, *args, **kwargs):
        self.repo.create_event(*args, **kwargs)

    def book_tickets(self, *args, **kwargs):
        self.repo.book_tickets(*args, **kwargs)

    def cancel_booking(self, booking_id):
        self.repo.cancel_booking(booking_id)

    def get_available_seats(self, event_name):
        self.repo.get_available_seats(event_name)

    def get_event_details(self, event_name):
        self.repo.get_event_details(event_name)

    def get_booking_details(self, booking_id):
        self.repo.get_booking_details(booking_id)

# TicketBookingSystem.py (Main Menu)
def main():
    service = BookingSystemServiceImpl()

    while True:
        print("""
======== Ticket Booking System ========
1. Create Event
2. Book Tickets
3. Cancel Booking
4. Get Available Seats
5. Get Event Details
6. Get Booking Details
7. Exit
        """)
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            continue

        if choice == 1:
            event_name = input("Event Name: ")
            date = input("Date (YYYY-MM-DD): ")
            time = input("Time (HH:MM:SS): ")
            total_seats = int(input("Total Seats: "))
            ticket_price = float(input("Ticket Price: "))
            event_type = input("Type (Movie/Sports/Concert): ")
            venue_name = input("Venue Name: ")
            venue_address = input("Venue Address: ")
            venue = Venue(venue_name, venue_address)
            service.create_event(event_name, date, time, total_seats, ticket_price, event_type, venue)

        elif choice == 2:
            ename = input("Enter Event Name: ")
            n = int(input("Number of tickets to book: "))
            customers = []
            for i in range(n):
                cname = input(f"Customer {i+1} Name: ")
                email = input(f"Customer {i+1} Email: ")
                phone = input(f"Customer {i+1} Phone: ")
                customers.append(Customer(cname, email, phone))
            service.book_tickets(ename, n, customers)

        elif choice == 3:
            booking_id = int(input("Enter Booking ID to cancel: "))
            service.cancel_booking(booking_id)

        elif choice == 4:
            ename = input("Enter Event Name: ")
            service.get_available_seats(ename)

        elif choice == 5:
            ename = input("Enter Event Name: ")
            service.get_event_details(ename)

        elif choice == 6:
            booking_id = int(input("Enter Booking ID: "))
            service.get_booking_details(booking_id)

        elif choice == 7:
            print("👋 Exiting the system...")
            break

        else:
            print("❌ Invalid choice. Please select from the menu options.")

if __name__ == "__main__":
    main()