class Route:
    def __init__(self, route_id=None, start_destination=None, end_destination=None, distance=None):
        self.__route_id = route_id
        self.__start_destination = start_destination
        self.__end_destination = end_destination
        self.__distance = distance

    def get_route_id(self):
        return self.__route_id

    def set_route_id(self, route_id):
        self.__route_id = route_id

    def get_start_destination(self):
        return self.__start_destination

    def set_start_destination(self, start_destination):
        self.__start_destination = start_destination

    def get_end_destination(self):
        return self.__end_destination

    def set_end_destination(self, end_destination):
        self.__end_destination = end_destination

    def get_distance(self):
        return self.__distance

    def set_distance(self, distance):
        self.__distance = distance