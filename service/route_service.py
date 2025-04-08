from dao.route_dao import RouteDAO
from entity.route import Route
from exceptions.exceptions import RouteNotFoundException, InvalidRouteDataException

class RouteService:
    def __init__(self):
        self.route_dao = RouteDAO()

    def add_route(self, route: Route) -> bool:
        # Validate route data
        if not route.get_start_destination() or not route.get_end_destination():
            raise InvalidRouteDataException("Start and end destinations cannot be empty.")
        if route.get_distance() <= 0:
            raise InvalidRouteDataException("Distance must be greater than 0.")

        # Add the route
        self.route_dao.add_route(route)
        return True

    def get_all_routes(self):
        return self.route_dao.get_all_routes()

    def get_route_by_id(self, route_id: int) -> Route:
        route = self.route_dao.get_route_by_id(route_id)
        if not route:
            raise RouteNotFoundException(f"Route with ID {route_id} not found.")
        return route

    def update_route(self, route: Route) -> bool:
        # Validate route data
        if not route.get_start_destination() or not route.get_end_destination():
            raise InvalidRouteDataException("Start and end destinations cannot be empty.")
        if route.get_distance() <= 0:
            raise InvalidRouteDataException("Distance must be greater than 0.")

        # Update the route
        self.route_dao.update_route(route)
        return True

    def delete_route(self, route_id: int) -> bool:
        route = self.route_dao.get_route_by_id(route_id)
        if not route:
            raise RouteNotFoundException(f"Route with ID {route_id} not found.")
        self.route_dao.delete_route(route_id)
        return True