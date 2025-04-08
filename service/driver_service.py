from dao.driver_dao import DriverDAO
from entity.driver import Driver
from exceptions.exceptions import DriverNotFoundException ,InvalidDriverDataException

class DriverService:
    def __init__(self):
        self.driver_dao = DriverDAO()

    def add_driver(self, driver: Driver) -> bool:
        # Validate driver data
        if not driver.get_name() or not driver.get_license_number() or not driver.get_phone_number():
            raise InvalidDriverDataException("Name, License Number, and Phone Number are required.")
        return self.driver_dao.add_driver(driver)

    def get_all_drivers(self):
        return self.driver_dao.get_all_drivers()

    def get_driver_by_id(self, driver_id: int) -> Driver:
        driver = self.driver_dao.get_driver_by_id(driver_id)
        if not driver:
            raise DriverNotFoundException(f"Driver with ID {driver_id} not found.")
        return driver

    def update_driver_status(self, driver_id: int, status: str) -> bool:
        driver = self.driver_dao.get_driver_by_id(driver_id)
        if not driver:
            raise DriverNotFoundException(f"Driver with ID {driver_id} not found.")
        self.driver_dao.update_driver_status(driver_id, status)
        return True

    def delete_driver(self, driver_id: int) -> bool:
        driver = self.driver_dao.get_driver_by_id(driver_id)
        if not driver:
            raise DriverNotFoundException(f"Driver with ID {driver_id} not found.")
        self.driver_dao.delete_driver(driver_id)
        return True