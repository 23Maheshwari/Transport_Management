from util.db_connection import DBConnUtil
from entity.trip import Trip

class TripDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()
        self.cursor = self.conn.cursor()

    def add_trip(self, trip: Trip):
        query = """
            INSERT INTO Trips (VehicleID, RouteID, DepartureDate, ArrivalDate, Status, TripType, MaxPassengers)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            trip.get_vehicle_id(),
            trip.get_route_id(),
            trip.get_departure_date(),
            trip.get_arrival_date(),
            trip.get_status(),
            trip.get_trip_type(),
            trip.get_max_passengers()
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_available_trips(self):
        query = """
            SELECT * FROM Trips
            WHERE Status = 'Scheduled' AND TripType = 'Passenger'
            ORDER BY DepartureDate ASC
        """
        self.cursor.execute(query)
        trips = self.cursor.fetchall()
        return trips
    def get_all_trips(self):
        query = "SELECT * FROM Trips"
        self.cursor.execute(query)
        trips = []
        for row in self.cursor.fetchall():
            trips.append(Trip(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        return trips

    def get_trip_by_id(self, trip_id: int):
        query = "SELECT * FROM Trips WHERE TripID = %s"
        self.cursor.execute(query, (trip_id,))
        row = self.cursor.fetchone()
        if row:
            return Trip(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        return None

    def update_trip(self, trip: Trip):
        query = """
            UPDATE Trips
            SET VehicleID = %s, RouteID = %s, DepartureDate = %s, ArrivalDate = %s, Status = %s, TripType = %s, MaxPassengers = %s
            WHERE TripID = %s
        """
        values = (
            trip.get_vehicle_id(),
            trip.get_route_id(),
            trip.get_departure_date(),
            trip.get_arrival_date(),
            trip.get_status(),
            trip.get_trip_type(),
            trip.get_max_passengers(),
            trip.get_trip_id()
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_trip(self, trip_id: int):
        query = "DELETE FROM Trips WHERE TripID = %s"
        self.cursor.execute(query, (trip_id,))
        self.conn.commit()

    def allocate_driver(self, trip_id: int, driver_id: int):
        # Allocate a driver to a trip
        query = "UPDATE Trips SET DriverID = %s WHERE TripID = %s"
        self.cursor.execute(query, (driver_id, trip_id))
        self.conn.commit()

    def deallocate_driver(self, trip_id: int):
        # Deallocate a driver from a trip
        query = "UPDATE Trips SET DriverID = NULL WHERE TripID = %s"
        self.cursor.execute(query, (trip_id,))
        self.conn.commit()

    def is_driver_available(self, driver_id: int) -> bool:
        # Check if a driver is available (not assigned to any active trip)
        query = """
            SELECT COUNT(*) FROM Trips
            WHERE DriverID = %s AND Status IN ('Scheduled', 'In Progress')
        """
        self.cursor.execute(query, (driver_id,))
        count = self.cursor.fetchone()[0]
        return count == 0