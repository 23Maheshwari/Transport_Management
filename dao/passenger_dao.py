from util.db_connection import DBConnUtil
from entity.passenger import Passenger

class PassengerDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()
        self.cursor = self.conn.cursor()

    def add_passenger(self, passenger: Passenger):
        query = "INSERT INTO Passengers (FirstName, Gender, Age, Email, PhoneNumber) VALUES (%s, %s, %s, %s, %s)"
        values = (
            passenger.get_first_name(),
            passenger.get_gender(),
            passenger.get_age(),
            passenger.get_email(),
            passenger.get_phone_number()
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_all_passengers(self):
        query = "SELECT * FROM Passengers"
        self.cursor.execute(query)
        passengers = []
        for row in self.cursor.fetchall():
            passengers.append(Passenger(row[0], row[1], row[2], row[3], row[4], row[5]))
        return passengers

    def get_passenger_by_id(self, passenger_id: int):
        query = "SELECT * FROM Passengers WHERE PassengerID = %s"
        self.cursor.execute(query, (passenger_id,))
        row = self.cursor.fetchone()
        if row:
            return Passenger(row[0], row[1], row[2], row[3], row[4], row[5])
        return None

    def update_passenger(self, passenger: Passenger):
        query = """
            UPDATE Passengers
            SET FirstName = %s, Gender = %s, Age = %s, Email = %s, PhoneNumber = %s
            WHERE PassengerID = %s
        """
        values = (
            passenger.get_first_name(),
            passenger.get_gender(),
            passenger.get_age(),
            passenger.get_email(),
            passenger.get_phone_number(),
            passenger.get_passenger_id()
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_passenger(self, passenger_id: int):
        query = "DELETE FROM Passengers WHERE PassengerID = %s"
        self.cursor.execute(query, (passenger_id,))
        self.conn.commit()