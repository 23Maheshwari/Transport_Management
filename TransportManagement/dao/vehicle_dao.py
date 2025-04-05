import mysql.connector
from entity.vehicle import Vehicle
from util.db_connection import DBConnUtil

class VehicleDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()
        self.cursor = self.conn.cursor()

    def add_vehicle(self, vehicle: Vehicle):
        query = "INSERT INTO Vehicle (vehicle_id, vehicle_number, capacity, vehicle_type) VALUES (%s, %s, %s, %s)"
        values = (
            vehicle.get_vehicle_id(),
            vehicle.get_vehicle_number(),
            vehicle.get_capacity(),
            vehicle.get_vehicle_type()
        )
        self.cursor.execute(query, values)
        self.conn.commit()
        print("✅ Vehicle added successfully!")

    def get_all_vehicles(self):
        query = "SELECT * FROM Vehicle"
        self.cursor.execute(query)
        vehicles = []
        for row in self.cursor.fetchall():
            v = Vehicle(row[0], row[1], row[2], row[3])
            vehicles.append(v)
        return vehicles

    def get_vehicle_by_id(self, vehicle_id: int):
        query = "SELECT * FROM Vehicle WHERE vehicle_id = %s"
        self.cursor.execute(query, (vehicle_id,))
        row = self.cursor.fetchone()
        if row:
            return Vehicle(row[0], row[1], row[2], row[3])
        return None
