from util.db_connection import DBConnUtil
from entity.booking import Booking

class BookingDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()
        self.cursor = self.conn.cursor()

    def book_ticket(self, booking: Booking):
        query = """
            INSERT INTO Bookings (TripID, PassengerID, BookingDate, Status)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            booking.get_trip_id(),
            booking.get_passenger_id(),
            booking.get_booking_date(),
            booking.get_status()
        )
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_bookings(self):
        query = "SELECT * FROM Bookings"
        self.cursor.execute(query)
        bookings = []
        for row in self.cursor.fetchall():
            bookings.append(Booking(row[0], row[1], row[2], row[3], row[4]))
        return bookings

    def get_booking_by_id(self, booking_id: int):
        query = "SELECT BookingID, TripID, PassengerID, BookingDate, Status FROM Bookings WHERE BookingID = %s"
        self.cursor.execute(query, (booking_id,))
        row = self.cursor.fetchone()
        if row:
            # Ensure the row has the expected number of fields
            if len(row) == 5:
                return Booking(row[0], row[1], row[2], row[3], row[4])
            else:
                raise ValueError(f"Unexpected row structure: {row}")
        return None

    def cancel_booking(self, booking_id: int):
        query = "UPDATE Bookings SET Status = 'Cancelled' WHERE BookingID = %s"
        self.cursor.execute(query, (booking_id,))
        self.conn.commit()

    def delete_booking(self, booking_id: int):
        query = "DELETE FROM Bookings WHERE BookingID = %s"
        self.cursor.execute(query, (booking_id,))
        self.conn.commit()
    
    def get_latest_booking_by_passenger_id(self, passenger_id: int):
        query = "SELECT * FROM Bookings WHERE PassengerID = %s ORDER BY BookingDate DESC LIMIT 1"
        self.cursor.execute(query, (passenger_id,))
        row = self.cursor.fetchone()
        if row:
            return Booking(row[0], row[1], row[2], row[3], row[4])
        return None
    
    def get_past_bookings_by_passenger_id(self, passenger_id: int):
        query = """
            SELECT b.BookingID, b.TripID, b.PassengerID, b.BookingDate, b.Status, t.DepartureDate, t.ArrivalDate, t.RouteID
            FROM Bookings b
            JOIN Trips t ON b.TripID = t.TripID
            WHERE b.PassengerID = %s AND b.Status IN ('Completed', 'Confirmed','Cancelled')
            ORDER BY b.BookingDate DESC
        """
        self.cursor.execute(query, (passenger_id,))
        return self.cursor.fetchall()