import unittest
from entity.driver import Driver
from entity.vehicle import Vehicle
from service.driver_vehicle_mapper import DriverVehicleMapper

class TestDriverVehicleMapping(unittest.TestCase):

    def test_driver_mapped_to_vehicle(self):
        driver = Driver(driver_id=1, name="Arun", license_number="DL12345", phone_number="9876543210", status="Active")
        vehicle = Vehicle(vehicle_id=101, model="Toyota", capacity=4, vehicle_type="SUV", status="Available")

        driver_vehicle_mapper = DriverVehicleMapper()
        driver_vehicle_mapper.assign_driver_to_vehicle(driver, vehicle)

        assigned_driver_id = driver_vehicle_mapper.get_driver_for_vehicle(vehicle)

        self.assertEqual(assigned_driver_id, 1)

        # Display the output after successful test using the getter method
        print(f"Driver {driver.get_name()} with ID {driver.get_driver_id()} is successfully mapped to vehicle {vehicle.get_model()} with vehicle ID {vehicle.get_vehicle_id()}.")

if __name__ == "__main__":
    unittest.main()
