import mysql.connector


class Event:
    def __init__(self, event_name=None, event_date=None, event_time=None, venue_name=None,
                 total_seats=0, available_seats=0, ticket_price=0.0, event_type=None):
        self.event_name = event_name
        self.event_date = event_date
        self.event_time = event_time
        self.venue_name = venue_name
        self.total_seats = total_seats
        self.available_seats = available_seats
        self.ticket_price = ticket_price
        self.event_type = event_type
    def get_event_name(self):
        return self.event_name

    def set_event_name(self, event_name):
        self.event_name = event_name


    def calculate_total_revenue(self):
        booked_tickets = self.total_seats - self.available_seats
        return booked_tickets * self.ticket_price

    def getBookedNoOfTickets(self):
        return self.total_seats - self.available_seats

    def book_tickets(self, num_tickets):
        if num_tickets <= self.available_seats:
            self.available_seats -= num_tickets
            print(f"{num_tickets} tickets booked successfully!")
        else:
            print("Not enough seats available!")

    def cancel_booking(self, num_tickets):
        if num_tickets <= (self.total_seats - self.available_seats):
            self.available_seats += num_tickets
            print(f"{num_tickets} tickets canceled successfully!")
        else:
            print("Cannot cancel more tickets than booked!")

    def display_event_details(self):
        print(f"Event Name: {self.event_name}")
        print(f"Date: {self.event_date}")
        print(f"Time: {self.event_time}")
        print(f"Venue: {self.venue_name}")
        print(f"Total Seats: {self.total_seats}")
        print(f"Available Seats: {self.available_seats}")
        print(f"Ticket Price: {self.ticket_price}")
        print(f"Event Type: {self.event_type}")
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="TicketBookingSystem"
    )
def fetch_event(event_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT event_name, event_date, event_time, venue_id, total_seats, available_seats, ticket_price, event_type FROM Event WHERE event_name = %s",
        (event_name,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return Event(*result)
    else:
        print("Event not found!")
        return None
event = fetch_event("Cricket Cup")
if event:
    event.display_event_details()
    event.book_tickets(5)
    print("Total Revenue:", event.calculate_total_revenue())
