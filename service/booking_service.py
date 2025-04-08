from dao.booking_dao import BookingDAO
from entity.booking import Booking
from exceptions import BookingNotFoundException ,InvalidBookingDataException

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

    def get_booking_by_id(self, booking_id: int, passenger_id: int) -> Booking:
        booking = self.booking_dao.get_booking_by_id(booking_id)
        if not booking:
            raise BookingNotFoundException(f"Booking with ID {booking_id} not found.")
        if booking.get_passenger_id() != passenger_id:
            raise InvalidBookingDataException("You can only access your own bookings.")
        return booking

    def cancel_booking(self, booking_id: int, passenger_id: int) -> bool:
        # Validate if the booking exists and belongs to the passenger
        booking = self.get_booking_by_id(booking_id, passenger_id)
        if booking.get_status() == 'Cancelled':
            raise InvalidBookingDataException("Booking is already cancelled.")
        
        # Cancel the booking
        self.booking_dao.cancel_booking(booking_id)
        return True

    def delete_booking(self, booking_id: int) -> bool:
        booking = self.booking_dao.get_booking_by_id(booking_id)
        if not booking:
            raise BookingNotFoundException(f"Booking with ID {booking_id} not found.")
        self.booking_dao.delete_booking(booking_id)
        return True

    def get_latest_booking_by_passenger_id(self, passenger_id: int):
        return self.booking_dao.get_latest_booking_by_passenger_id(passenger_id)
    
    def get_past_bookings_by_passenger_id(self, passenger_id: int):
        return self.booking_dao.get_past_bookings_by_passenger_id(passenger_id)