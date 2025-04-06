class Driver:
    def __init__(self, driver_id=None, name=None, license_number=None, phone_number=None, status=None):
        self.__driver_id = driver_id
        self.__name = name
        self.__license_number = license_number
        self.__phone_number = phone_number
        self.__status = status

    def get_driver_id(self):
        return self.__driver_id

    def set_driver_id(self, driver_id):
        self.__driver_id = driver_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_license_number(self):
        return self.__license_number

    def set_license_number(self, license_number):
        self.__license_number = license_number

    def get_phone_number(self):
        return self.__phone_number

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status