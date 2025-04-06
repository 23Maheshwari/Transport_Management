class RouteNotFoundException(Exception):
    """Raised when a route is not found in the database."""
    def __init__(self, message="Route not found"):
        super().__init__(message)

