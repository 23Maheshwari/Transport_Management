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
    
    def get_driver_trips(self, driver_id: int) -> list:
        """Get all trips assigned to a specific driver"""
        query = """
            SELECT t.* FROM Trips t
            WHERE t.DriverID = %s
            ORDER BY t.DepartureDate
        """
        self.cursor.execute(query, (driver_id,))
        return [Trip(*row) for row in self.cursor.fetchall()]

    def log_issue(self, driver_id: int, description: str, trip_id: int = None) -> bool:
        """Record driver issues in the database"""
        query = """
            INSERT INTO DriverIssues 
            (DriverID, TripID, Description, ReportedAt)
            VALUES (%s, %s, %s, NOW())
        """
        self.cursor.execute(query, (driver_id, trip_id, description))
        self.conn.commit()
        return True
    
    def get_trips_by_driver(self, driver_id: int):
        query = "SELECT * FROM Trips WHERE DriverID = %s"
        self.cursor.execute(query, (driver_id,))
        rows = self.cursor.fetchall()
        trips = []
        for row in rows:
            trip = Trip(
                trip_id=row[0],
                vehicle_id=row[1],
                route_id=row[2],
                departure_date=row[3],
                arrival_date=row[4],
                status=row[5],
                driver_id=row[6]
            )
            trips.append(trip)
        return trips
    
    def update_trip_status(self, trip_id: int, status: str) -> bool:
        try:
            conn = DBConnUtil.get_connection()
            cursor = conn.cursor()
            query = "UPDATE trips SET status = %s WHERE TripID = %s"
            cursor.execute(query, (status, trip_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"❌ Error updating trip status: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
