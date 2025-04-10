class TripNotFoundException(Exception):
    """Raised when a trip is not found."""
    def __init__(self, message="Trip not found"):
        super().__init__(message)


class InvalidTripDataException(Exception):
    """Raised when trip data is invalid."""
    def __init__(self, message="Invalid trip data"):
        super().__init__(message)

class InvalidRouteDataException(Exception):
    """Raised when trip data is invalid."""
    def __init__(self, message="Invalid route data"):
        super().__init__(message)
        
class DriverNotAvailableException(Exception):
    """Raised when a driver is not available."""
    def __init__(self, message="Driver not available"):
        super().__init__(message)

class DriverNotFoundException(Exception):
    """Raised when a not is not found."""
    def __init__(self, message="Driver not found"):
        super().__init__(message)

class PassengerNotFoundException(Exception):
    """Raised when a passenger is not found."""
    def __init__(self, message="Passenger not found"):
        super().__init__(message)


class VehicleNotFoundException(Exception):
    """Raised when a vehicle is not found."""
    def __init__(self, message="Vehicle not found"):
        super().__init__(message)

class RouteNotFoundException(Exception):
    """Raised when a vehicle is not found."""
    def __init__(self, message="Route not found"):
        super().__init__(message)

class InvalidPassengerDataException(Exception):
    """Raised when passenger data is invalid."""
    def __init__(self, message="Invalid passenger data"):
        super().__init__(message)


class InvalidDriverDataException(Exception):
    """Raised when driver data is invalid."""
    def __init__(self, message="Invalid driver data"):
        super().__init__(message)

class InvalidVehicleDataException(Exception):
    """Raised when driver data is invalid."""
    def __init__(self, message="Invalid vehicle data"):
        super().__init__(message)

class BookingNotFoundException(Exception):
    """Raised when driver data is invalid."""
    def __init__(self, message="Booking not found"):
        super().__init__(message)

class InvalidBookingDataException(Exception):
    """Raised when driver data is invalid."""
    def __init__(self, message="Invalid booking data"):
        super().__init__(message)