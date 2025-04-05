import mysql.connector
from db_connection import get_db_connection
from class_event import Event

class Booking:
    def __init__(self, booking_id, event_id, customer_id, num_tickets):
        self.booking_id = booking_id
        self.event_id = event_id
        self.customer_id = customer_id
        self.num_tickets = num_tickets
        self.total_cost = 0
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    def calculate_booking_cost(self):
        try:
            query = "SELECT ticket_price FROM event WHERE event_id = %s"
            self.cursor.execute(query, (self.event_id,))
            ticket_price = self.cursor.fetchone()[0]
            self.total_cost = ticket_price * self.num_tickets
            return self.total_cost
        except Exception as e:
            print(f"Error calculating booking cost: {e}")

    def book_tickets(self):

        try:

            query = "SELECT available_seats FROM event WHERE event_id = %s"
            self.cursor.execute(query, (self.event_id,))
            available_seats = self.cursor.fetchone()[0]

            if available_seats < self.num_tickets:
                print("❌ Not enough seats available!")
                return False


            update_query = "UPDATE event SET available_seats = available_seats - %s WHERE event_id = %s"
            self.cursor.execute(update_query, (self.num_tickets, self.event_id))


            insert_query = """INSERT INTO booking (booking_id, event_id, customer_id, num_tickets, total_cost) 
                              VALUES (%s, %s, %s, %s, %s)"""
            self.cursor.execute(insert_query, (self.booking_id, self.event_id, self.customer_id, self.num_tickets, self.total_cost))

            self.conn.commit()
            print("✅ Booking successful!")
            return True
        except Exception as e:
            print(f"Error booking tickets: {e}")
            self.conn.rollback()
            return False

    def cancel_booking(self):
        try:
            query = "SELECT num_tickets FROM booking WHERE booking_id = %s"
            self.cursor.execute(query, (self.booking_id,))
            result = self.cursor.fetchone()
            if not result:
                print("❌ Booking not found!")
                return False

            num_tickets = result[0]
            delete_query = "DELETE FROM booking WHERE booking_id = %s"
            self.cursor.execute(delete_query, (self.booking_id,))
            update_query = "UPDATE event SET available_seats = available_seats + %s WHERE event_id = %s"
            self.cursor.execute(update_query, (num_tickets, self.event_id))

            self.conn.commit()
            print("✅ Booking canceled successfully!")
            return True
        except Exception as e:
            print(f"Error canceling booking: {e}")
            self.conn.rollback()
            return False

    def getAvailableNoOfTickets(self):
        try:
            query = "SELECT available_seats FROM event WHERE event_id = %s"
            self.cursor.execute(query, (self.event_id,))
            available_tickets = self.cursor.fetchone()[0]
            return available_tickets
        except Exception as e:
            print(f"Error fetching available tickets: {e}")

    def getEventDetails(self):
        event = Event.fetch_event(self.event_id)
        return event
if __name__ == "__main__":
    booking = Booking(booking_id=11, event_id=2, customer_id=4, num_tickets=3)
    print(f"Total Cost: {booking.calculate_booking_cost()}")

    if booking.book_tickets():
        print(f"Remaining Tickets: {booking.getAvailableNoOfTickets()}")

    if booking.cancel_booking():
        print(f"Tickets After Cancellation: {booking.getAvailableNoOfTickets()}")
