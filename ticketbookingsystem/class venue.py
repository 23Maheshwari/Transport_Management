import mysql.connector
class Event:
    def __init__(self, event_name=None, event_date=None, event_time=None, venue_id=None,
                 total_seats=0, available_seats=0, ticket_price=0.0, event_type=None):
        self.event_name = event_name
        self.event_date = event_date
        self.event_time = event_time
        self.venue_id = venue_id
        self.total_seats = total_seats
        self.available_seats = available_seats
        self.ticket_price = ticket_price
        self.event_type = event_type

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
        print(f"Venue: {self.venue_id}")
        print(f"Total Seats: {self.total_seats}")
        print(f"Available Seats: {self.available_seats}")
        print(f"Ticket Price: {self.ticket_price}")
        print(f"Event Type: {self.event_type}")


class Venue:
    def __init__(self, venue_id=None, address=None):
        self.venue_id = venue_id
        self.address = address

    def display_venue_details(self):
        print(f"Venue id: {self.venue_id}")
        print(f"Address: {self.address}")
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
    select_query = """
        SELECT e.event_name, e.event_date, e.event_time, v.venue_name, 
               e.total_seats, e.available_seats, e.ticket_price, e.event_type
        FROM Event e
        JOIN Venue v ON e.venue_id = v.venue_id
        WHERE e.event_name = %s
    """

    cursor.execute(select_query, (event_name,))
    result = cursor.fetchone()
    conn.close()

    print("Fetched Data:", result)

    if result:
        return Event(*result)
    else:
        print("Event not found!")
        return None

event = fetch_event("IPL Final")
if event:
    event.display_event_details()
    event.book_tickets(5)
    print("Total Revenue:", event.calculate_total_revenue())
