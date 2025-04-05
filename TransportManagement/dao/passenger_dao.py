import mysql.connector
from entity.passenger import Passenger
from util.db_connection import DBConnUtil

class PassengerDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()
        self.cursor = self.conn.cursor()

    def add_passenger(self, passenger: Passenger):
        query = "INSERT INTO Passenger (passenger_id, name, age, gender, email) VALUES (%s, %s, %s, %s, %s)"
        values = (
            passenger.get_passenger_id(),
            passenger.get_name(),
            passenger.get_age(),
            passenger.get_gender(),
            passenger.get_email()
        )
        self.cursor.execute(query, values)
        self.conn.commit()
        print("✅ Passenger added successfully!")

    def get_all_passengers(self):
        query = "SELECT * FROM Passenger"
        self.cursor.execute(query)
        passengers = []
        for row in self.cursor.fetchall():
            p = Passenger(row[0], row[1], row[2], row[3], row[4])
            passengers.append(p)
        return passengers

    def get_passenger_by_id(self, passenger_id: int):
        query = "SELECT * FROM Passenger WHERE passenger_id = %s"
        self.cursor.execute(query, (passenger_id,))
        row = self.cursor.fetchone()
        if row:
            return Passenger(row[0], row[1], row[2], row[3], row[4])
        return None
