import mysql.connector
from util.db_connection import DBConnUtil
from entity.transport import Transport

class TransportDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()
        self.cursor = self.conn.cursor()

    def insert_transport(self, transport: Transport):
        query = "INSERT INTO transport (vehicle_number, vehicle_type, capacity) VALUES (%s, %s, %s)"
        values = (transport.vehicle_number, transport.vehicle_type, transport.capacity)
        self.cursor.execute(query, values)
        self.conn.commit()
        print("✅ Transport added successfully.")

    def get_all_transports(self):
        query = "SELECT * FROM transport"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        transports = []
        for row in result:
            transports.append(Transport(row[0], row[1], row[2], row[3]))
        return transports
