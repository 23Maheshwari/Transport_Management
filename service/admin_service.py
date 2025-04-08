from entity.trip import Trip
from entity.passenger import Passenger
from service.trip_service import TripService
from service.booking_service import BookingService
from service.passenger_service import PassengerService


class AdminService:
    def __init__(self):
        self.trip_service = TripService()
        self.booking_service = BookingService()
        self.passenger_service = PassengerService()

# ========================= Manage Trips =========================
    def add_trip(self):
        try:
            print("\n🚌 Add a New Trip:")
            vehicle_id = int(input("Enter Vehicle ID: "))
            route_id = int(input("Enter Route ID: "))
            departure_date = input("Enter Departure Date (YYYY-MM-DD HH:MM:SS): ")
            arrival_date = input("Enter Arrival Date (YYYY-MM-DD HH:MM:SS): ")
            status = "Scheduled"
            trip_type = input("Enter Trip Type (Passenger/Freight): ").capitalize()
            max_passengers = int(input("Enter Max Passengers: "))

            trip = Trip(None, vehicle_id, route_id, departure_date, arrival_date, status, trip_type, max_passengers)
            self.trip_service.add_trip(trip)
            print("✅ Trip added successfully!")
        except Exception as e:
            print(f"❌ Error adding trip: {e}")
            
    def update_trip(self):
        try:
            print("\n✏️ Update Trip Details:")
            trip_id = int(input("Enter Trip ID to update: "))
            trip = self.trip_service.get_trip_by_id(trip_id)
            if not trip:
                print(f"❌ Trip with ID {trip_id} not found.")
                return

            print("Leave fields blank to keep them unchanged.")
            new_departure_date = input(f"Enter new Departure Date (current: {trip.get_departure_date()}): ") or trip.get_departure_date()
            new_arrival_date = input(f"Enter new Arrival Date (current: {trip.get_arrival_date()}): ") or trip.get_arrival_date()
            new_status = input(f"Enter new Status (current: {trip.get_status()}): ") or trip.get_status()
            new_max_passengers = input(f"Enter new Max Passengers (current: {trip.get_max_passengers()}): ") or trip.get_max_passengers()

            trip.set_departure_date(new_departure_date)
            trip.set_arrival_date(new_arrival_date)
            trip.set_status(new_status)
            trip.set_max_passengers(int(new_max_passengers))

            self.trip_service.update_trip(trip)
            print("✅ Trip updated successfully!")
        except Exception as e:
            print(f"❌ Error updating trip: {e}")
            
    def delete_trip(self):
        try:
            print("\n🗑️ Delete a Trip:")
            trip_id = int(input("Enter Trip ID to delete: "))
            self.trip_service.delete_trip(trip_id)
            print(f"✅ Trip with ID {trip_id} deleted successfully!")
        except Exception as e:
            print(f"❌ Error deleting trip: {e}")
    
    def view_all_trips(self):
        try:
            print("\n🚌 All Trips:")
            trips = self.trip_service.get_all_trips()
            if trips:
                for trip in trips:
                    print(f"TripID: {trip.get_trip_id()}, VehicleID: {trip.get_vehicle_id()}, RouteID: {trip.get_route_id()}, "
                          f"DepartureDate: {trip.get_departure_date()}, ArrivalDate: {trip.get_arrival_date()}, "
                          f"Status: {trip.get_status()}, TripType: {trip.get_trip_type()}, MaxPassengers: {trip.get_max_passengers()}")
            else:
                print("❌ No trips found.")
        except Exception as e:
            print(f"❌ Error fetching trips: {e}")
            
# ========================= Manage Bookings =========================
    def view_all_bookings(self):
        try:
            print("\n📚 All Bookings:")
            bookings = self.booking_service.get_all_bookings()
            if bookings:
                for booking in bookings:
                    print(f"BookingID: {booking.get_booking_id()}, TripID: {booking.get_trip_id()}, "
                          f"PassengerID: {booking.get_passenger_id()}, BookingDate: {booking.get_booking_date()}, "
                          f"Status: {booking.get_status()}")
            else:
                print("❌ No bookings found.")
        except Exception as e:
            print(f"❌ Error fetching bookings: {e}")
    
    def cancel_booking(self):
        try:
            print("\n🛑 Cancel a Booking (Admin):")
            booking_id = int(input("Enter Booking ID to cancel: "))
            
            # Fetch the booking to ensure it exists
            booking = self.booking_service.booking_dao.get_booking_by_id(booking_id)
            if not booking:
                print(f"❌ Booking with ID {booking_id} not found.")
                return
            
            # Check if the booking is already cancelled
            if booking.get_status() == 'Cancelled':
                print(f"❌ Booking with ID {booking_id} is already cancelled.")
                return
            
            # Cancel the booking
            self.booking_service.booking_dao.cancel_booking(booking_id)
            print(f"✅ Booking with ID {booking_id} has been successfully canceled.")
        except Exception as e:
            print(f"❌ Error canceling booking: {e}")

    def delete_booking(self):
        try:
            print("\n🗑️ Delete a Booking:")
            booking_id = int(input("Enter Booking ID to delete: "))
            self.booking_service.delete_booking(booking_id)
            print(f"✅ Booking with ID {booking_id} has been successfully deleted.")
        except Exception as e:
            print(f"❌ Error deleting booking: {e}")
            
# ========================= Manage Passengers =========================

    def view_all_passengers(self):
        try:
            print("\n🧍‍♂️ All Registered Passengers:")
            passengers = self.passenger_service.get_all_passengers()
            if passengers:
                for passenger in passengers:
                    print(f"PassengerID: {passenger.get_passenger_id()}, Name: {passenger.get_first_name()}, "
                      f"Age: {passenger.get_age()}, Phone: {passenger.get_phone_number()}, "
                      f"Gender: {passenger.get_gender()}, Email: {passenger.get_email()}")
            else:
                print("❌ No passengers found.")
        except Exception as e:
            print(f"❌ Error fetching passengers: {e}")

    def add_passenger(self):
        try:
            print("\n📝 Add a New Passenger:")
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            phone_number = input("Enter Phone Number: ")
            gender = input("Enter Gender (Male/Female/Other): ").capitalize()
            email = input("Enter Email: ")

            passenger = Passenger(None, name, age, phone_number)
            passenger.set_gender(gender)
            passenger.set_email(email)

            self.passenger_service.add_passenger(passenger)
            print("✅ Passenger added successfully!")
        except Exception as e:
            print(f"❌ Error adding passenger: {e}")
    
    def update_passenger(self):
        try:
            print("\n✏️ Update Passenger Details:")
            passenger_id = int(input("Enter Passenger ID to update: "))
            passenger = self.passenger_service.get_passenger_by_id(passenger_id)
            if not passenger:
                print(f"❌ Passenger with ID {passenger_id} not found.")
                return

            print("Leave fields blank to keep them unchanged.")
            new_name = input(f"Enter new Name (current: {passenger.get_first_name()}): ") or passenger.get_first_name()
            new_email = input(f"Enter new Email (current: {passenger.get_email()}): ") or passenger.get_email()
            new_phone = input(f"Enter new Phone Number (current: {passenger.get_phone_number()}): ") or passenger.get_phone_number()

            passenger.set_first_name(new_name)
            passenger.set_email(new_email)
            passenger.set_phone_number(new_phone)

            self.passenger_service.update_passenger(passenger)
            print("✅ Passenger updated successfully!")
        except Exception as e:
            print(f"❌ Error updating passenger: {e}")
            
    def delete_passenger(self):
        try:
            print("\n🗑️ Delete a Passenger:")
            passenger_id = int(input("Enter Passenger ID to delete: "))
            self.passenger_service.delete_passenger(passenger_id)
            print(f"✅ Passenger with ID {passenger_id} has been successfully deleted.")
        except Exception as e:
            print(f"❌ Error deleting passenger: {e}")