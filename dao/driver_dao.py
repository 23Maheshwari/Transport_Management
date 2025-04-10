from util.db_connection import DBConnUtil
from entity.driver import Driver

class DriverDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()
        self.cursor = self.conn.cursor()

    def add_driver(self, driver: Driver):
        query = """
            INSERT INTO Drivers (Name, LicenseNumber, PhoneNumber, Status)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            driver.get_name(),
            driver.get_license_number(),
            driver.get_phone_number(),
            driver.get_status()
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_all_drivers(self):
        query = "SELECT * FROM Drivers"
        self.cursor.execute(query)
        drivers = []
        for row in self.cursor.fetchall():
            drivers.append(Driver(row[0], row[1], row[2], row[3], row[4]))
        return drivers

    def get_driver_by_id(self, driver_id: int):
        query = "SELECT * FROM Drivers WHERE DriverID = %s"
        self.cursor.execute(query, (driver_id,))
        row = self.cursor.fetchone()
        if row:
            return Driver(row[0], row[1], row[2], row[3], row[4])
        return None

    def update_driver(self, driver: Driver) -> bool:
        """Should update all driver fields"""
        query = """UPDATE Drivers SET 
                Name = %s, LicenseNumber = %s, 
                PhoneNumber = %s, Status = %s
                WHERE DriverID = %s"""
        values = (driver.get_name(), driver.get_license_number(),
                driver.get_phone_number(), driver.get_status(),
                driver.get_driver_id())
        self.cursor.execute(query, values)
        self.conn.commit()
        return True

    def delete_driver(self, driver_id: int):
        query = "DELETE FROM Drivers WHERE DriverID = %s"
        self.cursor.execute(query, (driver_id,))
        self.conn.commit()
        
    def get_driver_trips(self, driver_id: int):
        query = "SELECT * FROM Trips WHERE DriverID = %s"
        self.cursor.execute(query, (driver_id,))
        from entity.trip import Trip
        trips = []
        for row in self.cursor.fetchall():
            trips.append(Trip(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        return trips
    
    def start_trip(self, driver_id: int, trip_id: int):
        query = "UPDATE Trips SET Status = 'In Progress' WHERE TripID = %s AND DriverID = %s"
        self.cursor.execute(query, (trip_id, driver_id))
        self.conn.commit()

    def complete_trip(self, driver_id: int, trip_id: int):
        query = "UPDATE Trips SET Status = 'Completed' WHERE TripID = %s AND DriverID = %s"
        self.cursor.execute(query, (trip_id, driver_id))
        self.conn.commit()

    def report_issue(self, driver_id: int, issue: str, trip_id=None):
        query = """
            INSERT INTO DriverIssues (DriverID, TripID, Description)
            VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (driver_id, trip_id, issue))
        self.conn.commit()

    def log_issue(self, driver_id: int, issue: str, trip_id: int = None):
        query = """
            INSERT INTO DriverIssues (DriverID, TripID, Description)
            VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (driver_id, trip_id, issue))
        self.conn.commit()

    def update_driver_status(self, driver_id: int, status: str):
        query = "UPDATE Drivers SET Status = %s WHERE DriverID = %s"
        self.cursor.execute(query, (status, driver_id))
        self.conn.commit()
        
    def update_trip_status(self, trip_id: int, status: str):
        query = "UPDATE Trips SET Status = %s WHERE TripID = %s"
        self.cursor.execute(query, (status, trip_id))
        self.conn.commit()
        
    def get_driver_id_by_trip(self, trip_id: int):
        query = "SELECT DriverID FROM Trips WHERE TripID = %s"
        self.cursor.execute(query, (trip_id,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        return None

    def deallocate_driver(self, trip_id: int):
        query = "UPDATE Trips SET DriverID = NULL WHERE TripID = %s"
        self.cursor.execute(query, (trip_id,))
        self.conn.commit()
