class InvalidRouteDataException(Exception):
    """Raised when invalid data is provided for a route."""
    def __init__(self, message="Invalid route data"):
        super().__init__(message)