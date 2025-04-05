class Passenger:
    def __init__(self, passenger_id=None, first_name=None, gender=None, age=None, email=None, phone_number=None):
        self.__passenger_id = passenger_id
        self.__first_name = first_name
        self.__gender = gender
        self.__age = age
        self.__email = email
        self.__phone_number = phone_number

    def get_passenger_id(self):
        return self.__passenger_id

    def set_passenger_id(self, passenger_id):
        self.__passenger_id = passenger_id

    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def get_gender(self):
        return self.__gender

    def set_gender(self, gender):
        self.__gender = gender

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = age

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_phone_number(self):
        return self.__phone_number

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number
