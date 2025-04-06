class BookingNotFoundException(Exception):
    """Raised when a Booking is not found in the database."""
    def __init__(self, message="Booking not found"):
        super().__init__(message)