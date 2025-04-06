class TripNotFoundException(Exception):
    """Raised when invalid data is provided for a route."""
    def __init__(self, message="Trip not found"):
        super().__init__(message)