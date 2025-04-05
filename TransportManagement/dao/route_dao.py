import mysql.connector
from entity.route import Route
from util.db_connection import DBConnUtil

class RouteDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()
        self.cursor = self.conn.cursor()

    def add_route(self, route: Route):
        query = "INSERT INTO Route (route_id, source, destination, distance) VALUES (%s, %s, %s, %s)"
        values = (
            route.get_route_id(),
            route.get_source(),
            route.get_destination(),
            route.get_distance()
        )
        self.cursor.execute(query, values)
        self.conn.commit()
        print("✅ Route added successfully!")

    def get_all_routes(self):
        query = "SELECT * FROM Route"
        self.cursor.execute(query)
        routes = []
        for row in self.cursor.fetchall():
            r = Route(row[0], row[1], row[2], row[3])
            routes.append(r)
        return routes

    def get_route_by_id(self, route_id: int):
        query = "SELECT * FROM Route WHERE route_id = %s"
        self.cursor.execute(query, (route_id,))
        row = self.cursor.fetchone()
        if row:
            return Route(row[0], row[1], row[2], row[3])
        return None
