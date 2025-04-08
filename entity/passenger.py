class Passenger:

    def __init__(self, passenger_id=None, first_name=None, age=None, phone_number=None,gender=None, email=None):
        self.__passenger_id = passenger_id
        self.__first_name = first_name
        self.__age = age
        self.__phone_number = phone_number
        self.__gender = gender
        self.__email = email

    # Other methods remain unchanged

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
        if gender not in ['Male', 'Female', 'Other']:
            raise ValueError("Gender must be 'Male', 'Female', or 'Other'.")
        self.__gender = gender

    def get_age(self):
        return self.__age

    def set_age(self, age):
        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValueError("Age must be a valid integer between 0 and 120.")
        self.__age = age

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_phone_number(self):
        return self.__phone_number

    def set_phone_number(self, phone_number):
        if not phone_number.isdigit() or len(phone_number) < 10 or len(phone_number) > 15:
            raise ValueError("Phone number must be numeric and between 10 and 15 digits.")
        self.__phone_number = phone_number
    
    def __str__(self):
        return (f"PassengerID: {self.__passenger_id}, Name: {self.__first_name}, Gender: {self.__gender}, "
            f"Age: {self.__age}, Email: {self.__email}, Phone: {self.__phone_number}")
     