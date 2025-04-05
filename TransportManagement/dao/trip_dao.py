import mysql.connector
from entity.trip import Trip
from util.db_connection import DBConnUtil

class TripDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()
        self.cursor = self.conn.cursor()

    def add_trip(self, trip: Trip):
        query = "INSERT INTO Trip (trip_id, vehicle_id, route_id, departure_time, arrival_time, fare) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (
            trip.get_trip_id(),
            trip.get_vehicle_id(),
            trip.get_route_id(),
            trip.get_departure_time(),
            trip.get_arrival_time(),
            trip.get_fare()
        )
        self.cursor.execute(query, values)
        self.conn.commit()
        print("✅ Trip added successfully!")

    def get_all_trips(self):
        query = "SELECT * FROM Trip"
        self.cursor.execute(query)
        trips = []
        for row in self.cursor.fetchall():
            t = Trip(row[0], row[1], row[2], row[3], row[4], row[5])
            trips.append(t)
        return trips

    def get_trip_by_id(self, trip_id: int):
        query = "SELECT * FROM Trip WHERE trip_id = %s"
        self.cursor.execute(query, (trip_id,))
        row = self.cursor.fetchone()
        if row:
            return Trip(row[0], row[1], row[2], row[3], row[4], row[5])
        return None
