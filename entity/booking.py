class Booking:
    def __init__(self, booking_id=None, trip_id=None, passenger_id=None, booking_date=None, status=None):
        self.__booking_id = booking_id
        self.__trip_id = trip_id
        self.__passenger_id = passenger_id
        self.__booking_date = booking_date
        self.__status = status

    def get_booking_id(self):
        return self.__booking_id

    def set_booking_id(self, booking_id):
        self.__booking_id = booking_id

    def get_trip_id(self):
        return self.__trip_id

    def set_trip_id(self, trip_id):
        self.__trip_id = trip_id

    def get_passenger_id(self):
        return self.__passenger_id

    def set_passenger_id(self, passenger_id):
        self.__passenger_id = passenger_id

    def get_booking_date(self):
        return self.__booking_date

    def set_booking_date(self, booking_date):
        self.__booking_date = booking_date

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status
    
    def __str__(self):
        return (f"BookingID: {self.__booking_id}, TripID: {self.__trip_id}, "
                f"PassengerID: {self.__passenger_id}, BookingDate: {self.__booking_date}, "
                f"Status: {self.__status}")