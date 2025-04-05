class Vehicle:
    def __init__(self, vehicle_id=None, model=None, capacity=None, type=None, status=None):
        self.__vehicle_id = vehicle_id
        self.__model = model
        self.__capacity = capacity
        self.__type = type
        self.__status = status

    def get_vehicle_id(self):
        return self.__vehicle_id

    def set_vehicle_id(self, vehicle_id):
        self.__vehicle_id = vehicle_id

    def get_model(self):
        return self.__model

    def set_model(self, model):
        self.__model = model

    def get_capacity(self):
        return self.__capacity

    def set_capacity(self, capacity):
        self.__capacity = capacity

    def get_type(self):
        return self.__type

    def set_type(self, type):
        self.__type = type

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status