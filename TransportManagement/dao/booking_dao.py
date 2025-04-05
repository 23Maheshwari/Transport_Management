import mysql.connector
from entity.booking import Booking
from util.db_connection import DBConnUtil

class BookingDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()
        self.cursor = self.conn.cursor()

    def book_ticket(self, booking: Booking):
        query = """
            INSERT INTO Booking (booking_id, passenger_id, trip_id, booking_date, number_of_seats)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            booking.get_booking_id(),
            booking.get_passenger_id(),
            booking.get_trip_id(),
            booking.get_booking_date(),
            booking.get_number_of_seats()
        )
        self.cursor.execute(query, values)
        self.conn.commit()
        print("✅ Booking created successfully!")

    def get_all_bookings(self):
        query = "SELECT * FROM Booking"
        self.cursor.execute(query)
        bookings = []
        for row in self.cursor.fetchall():
            b = Booking(row[0], row[1], row[2], row[3], row[4])
            bookings.append(b)
        return bookings

    def get_booking_by_id(self, booking_id: int):
        query = "SELECT * FROM Booking WHERE booking_id = %s"
        self.cursor.execute(query, (booking_id,))
        row = self.cursor.fetchone()
        if row:
            return Booking(row[0], row[1], row[2], row[3], row[4])
        return None
