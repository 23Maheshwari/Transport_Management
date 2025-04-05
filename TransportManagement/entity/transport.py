class Transport:
    def __init__(self, transport_id=None, vehicle_number=None, vehicle_type=None, capacity=None):
        self._transport_id = transport_id
        self._vehicle_number = vehicle_number
        self._vehicle_type = vehicle_type
        self._capacity = capacity

    # Getter and Setter for transport_id
    def get_transport_id(self):
        return self._transport_id

    def set_transport_id(self, transport_id):
        self._transport_id = transport_id

    # Getter and Setter for vehicle_number
    def get_vehicle_number(self):
        return self._vehicle_number

    def set_vehicle_number(self, vehicle_number):
        self._vehicle_number = vehicle_number

    # Getter and Setter for vehicle_type
    def get_vehicle_type(self):
        return self._vehicle_type

    def set_vehicle_type(self, vehicle_type):
        self._vehicle_type = vehicle_type

    # Getter and Setter for capacity
    def get_capacity(self):
        return self._capacity

    def set_capacity(self, capacity):
        self._capacity = capacity

    # String representation
    def __str__(self):
        return f"Transport ID: {self._transport_id}, Vehicle Number: {self._vehicle_number}, Type: {self._vehicle_type}, Capacity: {self._capacity}"
