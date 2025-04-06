from dao.vehicle_dao import VehicleDAO
from entity.vehicle import Vehicle
from exceptions import VehicleNotFoundException, InvalidVehicleDataException

class VehicleService:
    def __init__(self):
        self.vehicle_dao = VehicleDAO()

    def add_vehicle(self, vehicle: Vehicle) -> bool:
        # Validate vehicle data
        if not vehicle.get_model() or not vehicle.get_vehicle_type() or not vehicle.get_status():
            raise InvalidVehicleDataException("Model, Type, and Status are required.")
        if vehicle.get_capacity() <= 0:
            raise InvalidVehicleDataException("Capacity must be a positive number.")
        if vehicle.get_vehicle_type() not in ['Truck', 'Van', 'Bus']:
            raise InvalidVehicleDataException("Invalid vehicle type. Allowed values: Truck, Van, Bus.")
        if vehicle.get_status() not in ['Available', 'On Trip', 'Maintenance']:
            raise InvalidVehicleDataException("Invalid vehicle status. Allowed values: Available, On Trip, Maintenance.")

        # Add the vehicle
        self.vehicle_dao.add_vehicle(vehicle)
        return True

    def get_all_vehicles(self):
        return self.vehicle_dao.get_all_vehicles()

    def get_vehicle_by_id(self, vehicle_id: int) -> Vehicle:
        vehicle = self.vehicle_dao.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            raise VehicleNotFoundException(f"Vehicle with ID {vehicle_id} not found.")
        return vehicle

    def update_vehicle(self, vehicle: Vehicle) -> bool:
        # Validate vehicle data
        if vehicle.get_capacity() <= 0:
            raise InvalidVehicleDataException("Capacity must be a positive number.")
        if vehicle.get_vehicle_type() not in ['Truck', 'Van', 'Bus']:
            raise InvalidVehicleDataException("Invalid vehicle type. Allowed values: Truck, Van, Bus.")
        if vehicle.get_status() not in ['Available', 'On Trip', 'Maintenance']:
            raise InvalidVehicleDataException("Invalid vehicle status. Allowed values: Available, On Trip, Maintenance.")

        # Update the vehicle
        self.vehicle_dao.update_vehicle(vehicle)
        return True

    def delete_vehicle(self, vehicle_id: int) -> bool:
        vehicle = self.vehicle_dao.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            raise VehicleNotFoundException(f"Vehicle with ID {vehicle_id} not found.")
        self.vehicle_dao.delete_vehicle(vehicle_id)
        return True