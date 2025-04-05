from dao.service_interface import TransportManagementService
from entity.vehicle import Vehicle
from entity.trip import Trip
from entity.booking import Booking
from entity.passenger import Passenger
from entity.route import Route
from util.db_connection import DBConnUtil
from myexceptions.custom_exceptions import VehicleNotFoundException, BookingNotFoundException
from typing import List
import mysql.connector


class TransportManagementServiceImpl(TransportManagementService):

    def __init__(self):
        self.conn = DBConnUtil.get_connection()

    def add_vehicle(self, vehicle: Vehicle) -> bool:
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO Vehicles (Model, Capacity, Type, Status) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (vehicle.model, vehicle.capacity, vehicle.type, vehicle.status))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error adding vehicle:", e)
            return False

    def update_vehicle(self, vehicle: Vehicle) -> bool:
        try:
            cursor = self.conn.cursor()
            sql = "UPDATE Vehicles SET Model=%s, Capacity=%s, Type=%s, Status=%s WHERE VehicleID=%s"
            cursor.execute(sql, (vehicle.model, vehicle.capacity, vehicle.type, vehicle.status, vehicle.vehicle_id))
            if cursor.rowcount == 0:
                raise VehicleNotFoundException("Vehicle ID not found for update.")
            self.conn.commit()
            return True
        except VehicleNotFoundException as e:
            print(e)
            return False
        except Exception as e:
            print("Error updating vehicle:", e)
            return False

    def delete_vehicle(self, vehicle_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            sql = "DELETE FROM Vehicles WHERE VehicleID=%s"
            cursor.execute(sql, (vehicle_id,))
            if cursor.rowcount == 0:
                raise VehicleNotFoundException("Vehicle ID not found for deletion.")
            self.conn.commit()
            return True
        except VehicleNotFoundException as e:
            print(e)
            return False
        except Exception as e:
            print("Error deleting vehicle:", e)
            return False

    # You can copy/paste or extend below for remaining functions
    def schedule_trip(self, vehicle_id: int, route_id: int, departure_date: str, arrival_date: str) -> bool:
        try:
            cursor = self.conn.cursor()
            sql = """INSERT INTO Trips (VehicleID, RouteID, DepartureDate, ArrivalDate, Status, TripType, MaxPassengers)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (vehicle_id, route_id, departure_date, arrival_date, "Scheduled", "Passenger", 40))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error scheduling trip:", e)
            return False

    def cancel_trip(self, trip_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            sql = "UPDATE Trips SET Status='Cancelled' WHERE TripID=%s"
            cursor.execute(sql, (trip_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error cancelling trip:", e)
            return False

    def book_trip(self, trip_id: int, passenger_id: int, booking_date: str) -> bool:
        try:
            cursor = self.conn.cursor()
            sql = """INSERT INTO Bookings (TripID, PassengerID, BookingDate, Status)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (trip_id, passenger_id, booking_date, "Confirmed"))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error booking trip:", e)
            return False

    def cancel_booking(self, booking_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            sql = "UPDATE Bookings SET Status='Cancelled' WHERE BookingID=%s"
            cursor.execute(sql, (booking_id,))
            if cursor.rowcount == 0:
                raise BookingNotFoundException("Booking not found.")
            self.conn.commit()
            return True
        except BookingNotFoundException as e:
            print(e)
            return False
        except Exception as e:
            print("Error cancelling booking:", e)
            return False

    def allocate_driver(self, trip_id: int, driver_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            sql = "UPDATE Trips SET DriverID=%s WHERE TripID=%s"
            cursor.execute(sql, (driver_id, trip_id))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error allocating driver:", e)
            return False

    def deallocate_driver(self, trip_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            sql = "UPDATE Trips SET DriverID=NULL WHERE TripID=%s"
            cursor.execute(sql, (trip_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error deallocating driver:", e)
            return False

    def get_bookings_by_passenger(self, passenger_id: int) -> List[Booking]:
        bookings = []
        try:
            cursor = self.conn.cursor(dictionary=True)
            sql = "SELECT * FROM Bookings WHERE PassengerID=%s"
            cursor.execute(sql, (passenger_id,))
            rows = cursor.fetchall()
            for row in rows:
                booking = Booking(**row)
                bookings.append(booking)
        except Exception as e:
            print("Error fetching bookings by passenger:", e)
        return bookings

    def get_bookings_by_trip(self, trip_id: int) -> List[Booking]:
        bookings = []
        try:
            cursor = self.conn.cursor(dictionary=True)
            sql = "SELECT * FROM Bookings WHERE TripID=%s"
            cursor.execute(sql, (trip_id,))
            rows = cursor.fetchall()
            for row in rows:
                booking = Booking(**row)
                bookings.append(booking)
        except Exception as e:
            print("Error fetching bookings by trip:", e)
        return bookings

    def get_available_drivers(self) -> List[int]:
        drivers = []
        try:
            cursor = self.conn.cursor()
            sql = """SELECT DriverID FROM Drivers WHERE DriverID NOT IN 
                     (SELECT DriverID FROM Trips WHERE DriverID IS NOT NULL)"""
            cursor.execute(sql)
            rows = cursor.fetchall()
            drivers = [row[0] for row in rows]
        except Exception as e:
            print("Error fetching available drivers:", e)
        return drivers
