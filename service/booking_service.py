from dao.booking_dao import BookingDAO
from entity.booking import Booking
from exceptions import BookingNotFoundException, InvalidBookingDataException

class BookingService:
    def __init__(self):
        self.booking_dao = BookingDAO()

    def book_ticket(self, booking: Booking) -> bool:
        # Validate booking data
        if not booking.get_trip_id() or not booking.get_passenger_id() or not booking.get_booking_date():
            raise InvalidBookingDataException("Trip ID, Passenger ID, and Booking Date are required.")
        if booking.get_status() not in ['Confirmed', 'Cancelled', 'Completed']:
            raise InvalidBookingDataException("Invalid booking status. Allowed values: Confirmed, Cancelled, Completed.")

        # Book the ticket
        self.booking_dao.book_ticket(booking)
        return True

    def get_all_bookings(self):
        return self.booking_dao.get_all_bookings()

    def get_booking_by_id(self, booking_id: int) -> Booking:
        booking = self.booking_dao.get_booking_by_id(booking_id)
        if not booking:
            raise BookingNotFoundException(f"Booking with ID {booking_id} not found.")
        return booking

    def cancel_booking(self, booking_id: int) -> bool:
        booking = self.booking_dao.get_booking_by_id(booking_id)
        if not booking:
            raise BookingNotFoundException(f"Booking with ID {booking_id} not found.")
        if booking.get_status() == 'Cancelled':
            raise InvalidBookingDataException("Booking is already cancelled.")
        self.booking_dao.cancel_booking(booking_id)
        return True

    def delete_booking(self, booking_id: int) -> bool:
        booking = self.booking_dao.get_booking_by_id(booking_id)
        if not booking:
            raise BookingNotFoundException(f"Booking with ID {booking_id} not found.")
        self.booking_dao.delete_booking(booking_id)
        return True