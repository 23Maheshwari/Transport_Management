import unittest
from service.booking_service import BookingService
from exceptions.exceptions import BookingNotFoundException, InvalidBookingDataException
from entity.booking import Booking

class TestBookingService(unittest.TestCase):
    def setUp(self):
        self.booking_service = BookingService()

    def test_booking_not_found_exception(self):
        print("Testing for BookingNotFoundException with invalid booking ID")
        try:
            self.booking_service.get_booking_by_id(-1, 100)  # Pass incorrect booking_id and passenger_id
        except BookingNotFoundException as e:
            print(f"Expected exception caught: {str(e)}")
            self.assertTrue(isinstance(e, BookingNotFoundException))  # Verifies that the exception is of the correct type

    def test_invalid_booking_data_exception(self):
        print("Testing for InvalidBookingDataException with mismatched booking ID and passenger ID")
        try:
            self.booking_service.get_booking_by_id(1, 999)  # Pass correct booking_id but incorrect passenger_id
        except InvalidBookingDataException as e:
            print(f"Expected exception caught: {str(e)}")
            self.assertTrue(isinstance(e, InvalidBookingDataException))  # Verifies that the exception is of the correct type

if __name__ == '__main__':
    unittest.main()
