import mysql.connector
from typing import List


class Venue:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address


class Event:
    def __init__(self, event_id: int, name: str, date: str, time: str, total_seats: int, ticket_price: float,
                 event_type: str, venue: Venue):
        self.event_id = event_id
        self.name = name
        self.date = date
        self.time = time
        self.total_seats = total_seats
        self.ticket_price = ticket_price
        self.event_type = event_type
        self.venue = venue
        self.booked_seats = 0
        self.booking_id = 1

    def calculate_booking_cost(self, num_tickets: int):
        return num_tickets * self.ticket_price

    def book_tickets(self, num_tickets: int, customers: List[str]):
        if self.booked_seats + num_tickets <= self.total_seats:
            for customer in customers:
                print(f"Booking ticket for {customer}")
                self.booked_seats += 1
            self.booking_id += 1
            print(f"Booking successful for {num_tickets} tickets.")
        else:
            print("Not enough seats available.")

    def cancel_booking(self, booking_id: int):
        if self.booked_seats > 0:
            self.booked_seats -= 1
            print(f"Booking {booking_id} canceled successfully.")
        else:
            print("No booking found to cancel.")

    def get_available_no_of_tickets(self):
        return self.total_seats - self.booked_seats

    def get_event_details(self):
        return f"Event Name: {self.name}, Date: {self.date}, Time: {self.time}, Venue: {self.venue.name}, Event Type: {self.event_type}"


class TicketBookingSystem:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ticketbookingsystem"
        )
        self.cursor = self.db.cursor()
        self.events = []
        self.load_events_from_db()

    def load_events_from_db(self):
        self.cursor.execute("SELECT * FROM event")
        events_data = self.cursor.fetchall()
        for event in events_data:
            venue = Venue(event[7], event[8])
            event_obj = Event(event[0], event[1], event[2], event[3], event[4], event[5], event[6], venue)
            self.events.append(event_obj)

    def create_event(self, event_name: str, date: str, time: str, total_seats: int, ticket_price: float,
                     event_type: str, venue: Venue):
        query = """
        INSERT INTO event (event_name, event_date, event_time, total_seats, ticket_price, event_type, venue_name, venue_address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (event_name, date, time, total_seats, ticket_price, event_type, venue.name, venue.address)
        self.cursor.execute(query, values)
        self.db.commit()

        event_id = self.cursor.lastrowid
        event = Event(event_id, event_name, date, time, total_seats, ticket_price, event_type, venue)
        self.events.append(event)
        print(f"🎟️ Event '{event_name}' has been successfully created!")

    def book_tickets(self, event_name: str, num_tickets: int, customers: List[str]):
        for event in self.events:
            if event.name == event_name:
                event.book_tickets(num_tickets, customers)
                return
        print("Event not found!")

    def cancel_tickets(self, booking_id: int):
        for event in self.events:
            event.cancel_booking(booking_id)

    def get_available_seats(self, event_name: str):
        for event in self.events:
            if event.name == event_name:
                return event.get_available_no_of_tickets()
        return "Event not found!"

    def get_event_details(self, event_name: str):
        for event in self.events:
            if event.name == event_name:
                return event.get_event_details()
        return "Event not found!"

    def main(self):
        while True:
            print("🎟️ Ticket Booking System Menu 🎟️")
            print("1. Create Event")
            print("2. Book Tickets")
            print("3. Cancel Tickets")
            print("4. Get Available Seats")
            print("5. Get Event Details")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                event_name = input("Enter event name: ")
                event_date = input("Enter event date (YYYY-MM-DD): ")
                event_time = input("Enter event time (HH:MM:SS): ")
                total_seats = int(input("Enter total seats: "))
                ticket_price = float(input("Enter ticket price: "))
                event_type = input("Enter event type (Movie/Sports/Concert): ")
                venue_name = input("Enter event venue: ")
                venue_address = input("Enter venue address: ")
                venue = Venue(venue_name, venue_address)
                self.create_event(event_name, event_date, event_time, total_seats, ticket_price, event_type, venue)

            elif choice == "2":
                event_name = input("Enter event name to book tickets: ")
                num_tickets = int(input("Enter number of tickets to book: "))
                customers = []
                for _ in range(num_tickets):
                    customer_name = input("Enter customer name: ")
                    customers.append(customer_name)
                self.book_tickets(event_name, num_tickets, customers)

            elif choice == "3":
                booking_id = int(input("Enter booking ID to cancel: "))
                self.cancel_tickets(booking_id)

            elif choice == "4":
                event_name = input("Enter event name to check available seats: ")
                available_seats = self.get_available_seats(event_name)
                print(f"Available Seats: {available_seats}")

            elif choice == "5":
                event_name = input("Enter event name to get event details: ")
                print(self.get_event_details(event_name))

            elif choice == "6":
                print("Exiting the system...")
                break


if __name__ == "__main__":
    system = TicketBookingSystem()
    system.main()
