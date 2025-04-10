# service/driver_service.py
from dao.driver_dao import DriverDAO
from entity.driver import Driver
from exceptions.exceptions import DriverNotFoundException, InvalidDriverDataException

class DriverService:
    def __init__(self):
        self.driver_dao = DriverDAO()

    # Core CRUD Operations
    def add_driver(self, driver: Driver) -> bool:
        """Add a new driver with validation"""
        self._validate_driver(driver)
        return self.driver_dao.add_driver(driver)

    def get_driver_by_id(self, driver_id: int) -> Driver:
        """Get driver by ID with existence check"""
        driver = self.driver_dao.get_driver_by_id(driver_id)
        if not driver:
            raise DriverNotFoundException(f"Driver with ID {driver_id} not found")
        return driver

    # Driver-Specific Functionalities
    def get_driver_trips(self, driver_id: int) -> list:
        """Get all trips assigned to a specific driver"""
        driver = self.get_driver_by_id(driver_id)
        return self.driver_dao.get_driver_trips(driver_id)

    def start_trip(self, driver_id: int, trip_id: int) -> bool:
        """Mark trip as started and update driver status"""
        self._validate_driver_status(driver_id, allowed_statuses=['Available'])
        self.driver_dao.update_driver_status(driver_id, "Assigned")
        return True

    def complete_trip(self, driver_id: int, trip_id: int) -> bool:
        """Mark trip as completed and update driver status"""
        self._validate_driver_status(driver_id, allowed_statuses=['Assigned'])
        self.driver_dao.update_driver_status(driver_id, "Available")
        return True

    def report_issue(self, driver_id: int, description: str, trip_id: int = None) -> bool:
        """Record driver-reported issues"""
        self.get_driver_by_id(driver_id)  # Verify driver exists
        return self.driver_dao.log_issue(driver_id, description, trip_id)

    # Helper Methods
    def _validate_driver(self, driver: Driver):
        """Validate driver data"""
        if not driver.get_name():
            raise InvalidDriverDataException("Driver name is required")
        if not driver.get_license_number():
            raise InvalidDriverDataException("License number is required")
        if driver.get_status() not in ['Available', 'Assigned', 'Inactive']:
            raise InvalidDriverDataException("Invalid status")

    def _validate_driver_status(self, driver_id: int, allowed_statuses: list):
        """Verify driver is in correct status for action"""
        driver = self.get_driver_by_id(driver_id)
        if driver.get_status() not in allowed_statuses:
            raise InvalidDriverDataException(
                f"Driver must be in status: {', '.join(allowed_statuses)}"
            )
    
    def get_all_drivers(self):
        return self.driver_dao.get_all_drivers()
    
    def update_driver(self, driver):
        return self.driver_dao.update_driver(driver)
    
    def delete_driver(self, driver_id: int):
        self.driver_dao.delete_driver(driver_id)