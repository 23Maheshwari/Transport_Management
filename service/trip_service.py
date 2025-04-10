#service\trip_service.py

from dao.trip_dao import TripDAO
from entity.trip import Trip
from exceptions.exceptions import TripNotFoundException, InvalidTripDataException, DriverNotAvailableException,DriverNotFoundException
from service.driver_service import DriverService
from dao.driver_dao import DriverDAO


class TripService:
    def __init__(self):
        self.trip_dao = TripDAO()
        self.driver_service = DriverService()
        self.driver_dao = DriverDAO() 

    def add_trip(self, trip: Trip) -> bool:
        # Validate trip data
        if not trip.get_vehicle_id() or not trip.get_route_id() or not trip.get_departure_date() or not trip.get_arrival_date():
            raise InvalidTripDataException("Vehicle ID, Route ID, Departure Date, and Arrival Date are required.")
        if trip.get_departure_date() >= trip.get_arrival_date():
            raise InvalidTripDataException("Departure date must be before arrival date.")
        if trip.get_status() not in ['Scheduled', 'In Progress', 'Completed', 'Cancelled']:
            raise InvalidTripDataException("Invalid trip status.")
        if trip.get_trip_type() not in ['Freight', 'Passenger']:
            raise InvalidTripDataException("Invalid trip type.")
        if trip.get_max_passengers() < 0:
            raise InvalidTripDataException("MaxPassengers must be a non-negative number.")

        # Add the trip
        self.trip_dao.add_trip(trip)
        return True

    def get_all_trips(self):
        return self.trip_dao.get_all_trips()

    def get_trip_by_id(self, trip_id: int) -> Trip:
        trip = self.trip_dao.get_trip_by_id(trip_id)
        if not trip:
            raise TripNotFoundException(f"Trip with ID {trip_id} not found.")
        return trip

    def update_trip(self, trip: Trip) -> bool:
    # Validate trip data
        if trip.get_departure_date() >= trip.get_arrival_date():
            raise InvalidTripDataException("Departure date must be before arrival date.")
        if trip.get_status() not in ['Scheduled', 'In Progress', 'Completed', 'Cancelled']:
            raise InvalidTripDataException("Invalid trip status.")
        if trip.get_trip_type() not in ['Freight', 'Passenger']:
            raise InvalidTripDataException("Invalid trip type.")
        if trip.get_max_passengers() < 0:
            raise InvalidTripDataException("MaxPassengers must be a non-negative number.")

        # Update the trip
        self.trip_dao.update_trip(trip)

        # Update driver availability based on trip status
        if trip.get_driver_id():
            if trip.get_status() in ['Scheduled', 'In Progress']:
                self.driver_service.update_driver_status(trip.get_driver_id(), 'Assigned')
            elif trip.get_status() in ['Completed', 'Cancelled']:
                self.driver_service.update_driver_status(trip.get_driver_id(), 'Available')

        return True

    def delete_trip(self, trip_id: int) -> bool:
        trip = self.trip_dao.get_trip_by_id(trip_id)
        if not trip:
            raise TripNotFoundException(f"Trip with ID {trip_id} not found.")
        self.trip_dao.delete_trip(trip_id)
        return True

    # Add to trip_service.py
    def allocate_driver(self, trip_id: int, driver_id: int) -> bool:
        # Check trip exists
        trip = self.get_trip_by_id(trip_id)
        if not trip:
            raise TripNotFoundException(f"Trip {trip_id} not found")
        
        # Check driver exists and is available
        driver = self.driver_service.get_driver_by_id(driver_id)
        if not driver:
            raise DriverNotFoundException(f"Driver {driver_id} not found")
        if not self.is_driver_available(driver_id):
            raise DriverNotAvailableException(f"Driver {driver_id} is already assigned")
        
        # Update both trip and driver status
        self.trip_dao.allocate_driver(trip_id, driver_id)
        return True

    def deallocate_driver(self, trip_id: int) -> bool:
        driver_id = self.driver_dao.get_driver_id_by_trip(trip_id)
        if not driver_id:
            raise DriverNotFoundException("No driver assigned to this trip")

        self.driver_dao.deallocate_driver(trip_id)
        self.driver_dao.update_driver_status(driver_id, "Available")

        # ❗ Remove the driver from the trip record
        self.trip_dao.allocate_driver(trip_id, None)  # This must set driver_id to NULL in Trips table

        return True

    def update_trip_status(self, trip_id: int, status: str):
        return self.trip_dao.update_trip_status(trip_id, status)
    
    def is_driver_available(self, driver_id: int) -> bool:
        driver = self.driver_dao.get_driver_by_id(driver_id)
        return driver is not None and driver.get_status().lower() == "available"