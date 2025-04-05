class Trip:
    def __init__(self, trip_id=None, vehicle_id=None, route_id=None, departure_date=None, arrival_date=None, status=None, trip_type='Freight', max_passengers=None):
        self.__trip_id = trip_id
        self.__vehicle_id = vehicle_id
        self.__route_id = route_id
        self.__departure_date = departure_date
        self.__arrival_date = arrival_date
        self.__status = status
        self.__trip_type = trip_type
        self.__max_passengers = max_passengers

    def get_trip_id(self):
        return self.__trip_id

    def set_trip_id(self, trip_id):
        self.__trip_id = trip_id

    def get_vehicle_id(self):
        return self.__vehicle_id

    def set_vehicle_id(self, vehicle_id):
        self.__vehicle_id = vehicle_id

    def get_route_id(self):
        return self.__route_id

    def set_route_id(self, route_id):
        self.__route_id = route_id

    def get_departure_date(self):
        return self.__departure_date

    def set_departure_date(self, departure_date):
        self.__departure_date = departure_date

    def get_arrival_date(self):
        return self.__arrival_date

    def set_arrival_date(self, arrival_date):
        self.__arrival_date = arrival_date

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def get_trip_type(self):
        return self.__trip_type

    def set_trip_type(self, trip_type):
        self.__trip_type = trip_type

    def get_max_passengers(self):
        return self.__max_passengers

    def set_max_passengers(self, max_passengers):
        self.__max_passengers = max_passengers
