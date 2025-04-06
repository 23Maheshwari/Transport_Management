from util.db_connection import DBConnUtil
from entity.vehicle import Vehicle

class VehicleDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()
        self.cursor = self.conn.cursor()

    def add_vehicle(self, vehicle: Vehicle):
        query = """
            INSERT INTO Vehicles (Model, Capacity, Type, Status)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            vehicle.get_model(),
            vehicle.get_capacity(),
            vehicle.get_vehicle_type(),
            vehicle.get_status()
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_all_vehicles(self):
        query = "SELECT * FROM Vehicles"
        self.cursor.execute(query)
        vehicles = []
        for row in self.cursor.fetchall():
            vehicles.append(Vehicle(row[0], row[1], row[2], row[3], row[4]))
        return vehicles

    def get_vehicle_by_id(self, vehicle_id: int):
        query = "SELECT * FROM Vehicles WHERE VehicleID = %s"
        self.cursor.execute(query, (vehicle_id,))
        row = self.cursor.fetchone()
        if row:
            return Vehicle(row[0], row[1], row[2], row[3], row[4])
        return None

    def update_vehicle(self, vehicle: Vehicle):
        query = """
            UPDATE Vehicles
            SET Model = %s, Capacity = %s, Type = %s, Status = %s
            WHERE VehicleID = %s
        """
        values = (
            vehicle.get_model(),
            vehicle.get_capacity(),
            vehicle.get_vehicle_type(),
            vehicle.get_status(),
            vehicle.get_vehicle_id()
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_vehicle(self, vehicle_id: int):
        query = "DELETE FROM Vehicles WHERE VehicleID = %s"
        self.cursor.execute(query, (vehicle_id,))
        self.conn.commit()