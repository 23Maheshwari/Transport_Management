from util.db_connection import DBConnUtil
from entity.route import Route

class RouteDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()
        self.cursor = self.conn.cursor()

    def add_route(self, route: Route):
        query = """
            INSERT INTO Routes (StartDestination, EndDestination, Distance)
            VALUES (%s, %s, %s)
        """
        values = (
            route.get_start_destination(),
            route.get_end_destination(),
            route.get_distance()
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_all_routes(self):
        query = "SELECT * FROM Routes"
        self.cursor.execute(query)
        routes = []
        for row in self.cursor.fetchall():
            routes.append(Route(row[0], row[1], row[2], row[3]))
        return routes

    def get_route_by_id(self, route_id: int):
        query = "SELECT * FROM Routes WHERE RouteID = %s"
        self.cursor.execute(query, (route_id,))
        row = self.cursor.fetchone()
        if row:
            return Route(row[0], row[1], row[2], row[3])
        return None

    def update_route(self, route: Route):
        query = """
            UPDATE Routes
            SET StartDestination = %s, EndDestination = %s, Distance = %s
            WHERE RouteID = %s
        """
        values = (
            route.get_start_destination(),
            route.get_end_destination(),
            route.get_distance(),
            route.get_route_id()
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_route(self, route_id: int):
        query = "DELETE FROM Routes WHERE RouteID = %s"
        self.cursor.execute(query, (route_id,))
        self.conn.commit()