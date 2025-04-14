import unittest
from entity.booking import Booking
from service.booking_service import BookingService

class TestBookingFunctionality(unittest.TestCase):
    def setUp(self):
        self.booking_service = BookingService()

    def test_booking_success(self):
        booking = Booking(None, trip_id=1, passenger_id=10, booking_date="2025-04-14", status="Confirmed")
        booking_id = self.booking_service.book_ticket(booking)
        self.assertIsNotNone(booking_id)
        print(f"Booking successful! Booking ID: {booking_id}")

if __name__ == '__main__':
    unittest.main()
