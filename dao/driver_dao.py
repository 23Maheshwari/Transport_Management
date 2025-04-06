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

    def update_driver_status(self, driver_id: int, status: str):
        query = "UPDATE Drivers SET Status = %s WHERE DriverID = %s"
        self.cursor.execute(query, (status, driver_id))
        self.conn.commit()

    def delete_driver(self, driver_id: int):
        query = "DELETE FROM Drivers WHERE DriverID = %s"
        self.cursor.execute(query, (driver_id,))
        self.conn.commit()