from entity.trip import Trip
from entity.passenger import Passenger
from service.trip_service import TripService
from service.booking_service import BookingService
from service.passenger_service import PassengerService
from service.vehicle_service import VehicleService
from entity.vehicle import Vehicle
from exceptions.exceptions import VehicleNotFoundException, InvalidVehicleDataException
from service.route_service import RouteService
from entity.route import Route
from exceptions.exceptions import RouteNotFoundException, InvalidRouteDataException
from datetime import datetime
from collections import defaultdict
from exceptions.exceptions import DriverNotFoundException, InvalidDriverDataException
from service.driver_service import DriverService
from entity.driver import Driver

class AdminService:
    def __init__(self):
        self.trip_service = TripService()
        self.booking_service = BookingService()
        self.passenger_service = PassengerService()
        self.vehicle_service = VehicleService()
        self.route_service = RouteService()
        self.driver_service = DriverService() 

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

 # ======================== Manage Vehicles ========================
    def add_vehicle(self):
        try:
            print("\n🚗 Add a New Vehicle:")
            model = input("Enter Model: ")
            capacity = float(input("Enter Capacity: "))
            vehicle_type = input("Enter Type (Truck/Van/Bus): ").capitalize()
            status = input("Enter Status (Available/On Trip/Maintenance): ").capitalize()

            vehicle = Vehicle(None, model, capacity, vehicle_type, status)
            self.vehicle_service.add_vehicle(vehicle)
            print("✅ Vehicle added successfully!")
        except InvalidVehicleDataException as e:
            print(f"❌ Validation error: {e}")
        except Exception as e:
            print(f"❌ Error adding vehicle: {e}")

    def update_vehicle(self):
        try:
            print("\n✏️ Update Vehicle Details:")
            vehicle_id = int(input("Enter Vehicle ID to update: "))
            vehicle = self.vehicle_service.get_vehicle_by_id(vehicle_id)
            if not vehicle:
                print(f"❌ Vehicle with ID {vehicle_id} not found.")
                return

            print("Leave fields blank to keep current value.")
            new_model = input(f"Enter new Model (current: {vehicle.get_model()}): ") or vehicle.get_model()
            new_capacity = input(f"Enter new Capacity (current: {vehicle.get_capacity()}): ")
            new_capacity = float(new_capacity) if new_capacity else vehicle.get_capacity()
            new_type = input(f"Enter new Type (current: {vehicle.get_vehicle_type()}): ").title() or vehicle.get_vehicle_type()
            
            # Fix for status input - use title() instead of capitalize()
            current_status = vehicle.get_status()
            status_input = input(f"Enter new Status (current: {current_status}): ")
            new_status = status_input.title() if status_input else current_status

            vehicle.set_model(new_model)
            vehicle.set_capacity(new_capacity)
            vehicle.set_vehicle_type(new_type)
            vehicle.set_status(new_status)

            self.vehicle_service.update_vehicle(vehicle)
            print("✅ Vehicle updated successfully!")
        except VehicleNotFoundException as e:
            print(f"❌ {e}")
        except InvalidVehicleDataException as e:
            print(f"❌ Validation error: {e}")
        except Exception as e:
            print(f"❌ Error updating vehicle: {e}")
            
    def delete_vehicle(self):
        try:
            print("\n🗑️ Delete a Vehicle:")
            vehicle_id = int(input("Enter Vehicle ID to delete: "))
            self.vehicle_service.delete_vehicle(vehicle_id)
            print(f"✅ Vehicle with ID {vehicle_id} deleted successfully!")
        except VehicleNotFoundException as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error deleting vehicle: {e}")

    def view_all_vehicles(self):
        try:
            print("\n🚗 All Vehicles:")
            vehicles = self.vehicle_service.get_all_vehicles()
            if vehicles:
                for vehicle in vehicles:
                    print(f"VehicleID: {vehicle.get_vehicle_id()}, Model: {vehicle.get_model()}, "
                          f"Type: {vehicle.get_vehicle_type()}, Capacity: {vehicle.get_capacity()}, "
                          f"Status: {vehicle.get_status()}")
            else:
                print("❌ No vehicles found.")
        except Exception as e:
            print(f"❌ Error fetching vehicles: {e}")
            
        # ======================== Manage Routes ========================
    def add_route(self):
        try:
            print("\n🛣️ Add a New Route:")
            start = input("Enter Start Destination: ")
            end = input("Enter End Destination: ")
            distance = float(input("Enter Distance (km): "))

            route = Route(None, start, end, distance)
            self.route_service.add_route(route)
            print("✅ Route added successfully!")
        except InvalidRouteDataException as e:
            print(f"❌ Validation error: {e}")
        except Exception as e:
            print(f"❌ Error adding route: {e}")

    def update_route(self):
        try:
            print("\n✏️ Update Route Details:")
            route_id = int(input("Enter Route ID to update: "))
            route = self.route_service.get_route_by_id(route_id)
            if not route:
                print(f"❌ Route with ID {route_id} not found.")
                return

            print("Leave fields blank to keep current value.")
            new_start = input(f"Enter new Start (current: {route.get_start_destination()}): ") or route.get_start_destination()
            new_end = input(f"Enter new End (current: {route.get_end_destination()}): ") or route.get_end_destination()
            new_distance = input(f"Enter new Distance (current: {route.get_distance()} km): ")
            new_distance = float(new_distance) if new_distance else route.get_distance()

            route.set_start_destination(new_start)
            route.set_end_destination(new_end)
            route.set_distance(new_distance)

            self.route_service.update_route(route)
            print("✅ Route updated successfully!")
        except RouteNotFoundException as e:
            print(f"❌ {e}")
        except InvalidRouteDataException as e:
            print(f"❌ Validation error: {e}")
        except Exception as e:
            print(f"❌ Error updating route: {e}")

    def delete_route(self):
        try:
            print("\n🗑️ Delete a Route:")
            route_id = int(input("Enter Route ID to delete: "))
            self.route_service.delete_route(route_id)
            print(f"✅ Route with ID {route_id} deleted successfully!")
        except RouteNotFoundException as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error deleting route: {e}")

    def view_all_routes(self):
        try:
            print("\n🛣️ All Routes:")
            routes = self.route_service.get_all_routes()
            if routes:
                for route in routes:
                    print(f"RouteID: {route.get_route_id()}, "
                          f"{route.get_start_destination()} → {route.get_end_destination()}, "
                          f"Distance: {route.get_distance()} km")
            else:
                print("❌ No routes found.")
        except Exception as e:
            print(f"❌ Error fetching routes: {e}")
            
    # ======================== Reports and Analytics ========================
    def view_booking_stats(self):
        try:
            print("\n📊 Booking Statistics:")
            bookings = self.booking_service.booking_dao.get_all_bookings()
            
            total = len(bookings)
            cancelled = sum(1 for b in bookings if b.get_status() == 'Cancelled')
            completed = sum(1 for b in bookings if b.get_status() == 'Completed')
            
            print(f"Total Bookings: {total}")
            print(f"Cancelled Bookings: {cancelled} ({cancelled/total*100:.1f}%)")
            print(f"Completed Trips: {completed} ({completed/total*100:.1f}%)")
            
        except Exception as e:
            print(f"❌ Error generating booking stats: {e}")

    def view_revenue_reports(self):
        try:
            print("\n💰 Revenue Reports:")
            # Assuming each booking generates $50 revenue (adjust as needed)
            bookings = self.booking_service.booking_dao.get_all_bookings()
            confirmed_bookings = [b for b in bookings if b.get_status() == 'Confirmed']
            revenue = len(confirmed_bookings) * 50
            
            print(f"Total Confirmed Bookings: {len(confirmed_bookings)}")
            print(f"Estimated Revenue: ${revenue}")
            
            # Monthly breakdown - fixed datetime handling
            monthly_revenue = defaultdict(int)
            for booking in confirmed_bookings:
                booking_date = booking.get_booking_date()
                # Handle both string and datetime objects
                if isinstance(booking_date, str):
                    month = datetime.strptime(booking_date, "%Y-%m-%d %H:%M:%S").strftime("%B %Y")
                else:  # Assume it's a datetime object
                    month = booking_date.strftime("%B %Y")
                monthly_revenue[month] += 50
            
            print("\nMonthly Breakdown:")
            for month, amount in sorted(monthly_revenue.items()):
                print(f"{month}: ${amount}")
                
        except Exception as e:
            print(f"❌ Error generating revenue report: {e}")

    def view_passenger_activity(self):
        try:
            print("\n👥 Passenger Activity:")
            bookings = self.booking_service.booking_dao.get_all_bookings()
            passenger_counts = defaultdict(int)
            
            for booking in bookings:
                passenger_counts[booking.get_passenger_id()] += 1
            
            # Get top 5 passengers
            sorted_passengers = sorted(passenger_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            print("Top 5 Most Active Passengers:")
            for passenger_id, count in sorted_passengers:
                passenger = self.passenger_service.get_passenger_by_id(passenger_id)
                print(f"{passenger.get_first_name()} (ID: {passenger_id}): {count} bookings")
                
        except Exception as e:
            print(f"❌ Error generating passenger activity: {e}")

    def view_trip_utilization(self):
        try:
            print("\n🚌 Trip Utilization:")
            trips = self.trip_service.get_all_trips()
            bookings = self.booking_service.booking_dao.get_all_bookings()
            
            print("Trip ID | Utilization | Status")
            print("--------------------------------")
            for trip in trips:
                if trip.get_trip_type() == 'Passenger' and trip.get_max_passengers() > 0:
                    trip_bookings = sum(1 for b in bookings 
                                      if b.get_trip_id() == trip.get_trip_id() 
                                      and b.get_status() == 'Confirmed')
                    utilization = (trip_bookings / trip.get_max_passengers()) * 100
                    print(f"{trip.get_trip_id():<7} | {utilization:>6.1f}%    | {trip.get_status()}")
                    
        except Exception as e:
            print(f"❌ Error generating trip utilization: {e}")
            
    # ======================== Driver Management ========================
    def add_driver(self):
        try:
            print("\n👨‍✈️ Add New Driver:")
            name = input("Enter Driver Name: ")
            license = input("Enter License Number: ")
            phone = input("Enter Phone Number: ")
            
            driver = Driver(None, name, license, phone, "Available")
            self.driver_service.add_driver(driver)
            print("✅ Driver added successfully!")
        except InvalidDriverDataException as e:
            print(f"❌ Validation error: {e}")
        except Exception as e:
            print(f"❌ Error adding driver: {e}")

    def update_driver(self):
        try:
            print("\n✏️ Update Driver Details:")
            driver_id = int(input("Enter Driver ID to update: "))
            driver = self.driver_service.get_driver_by_id(driver_id)
            if not driver:
                print(f"❌ Driver with ID {driver_id} not found.")
                return

            print("Leave blank to keep current value.")
            new_name = input(f"Name (current: {driver.get_name()}): ") or driver.get_name()
            new_license = input(f"License (current: {driver.get_license_number()}): ") or driver.get_license_number()
            new_phone = input(f"Phone (current: {driver.get_phone_number()}): ") or driver.get_phone_number()
            new_status = input(f"Status (current: {driver.get_status()}): ").title() or driver.get_status()

            driver.set_name(new_name)
            driver.set_license_number(new_license)
            driver.set_phone_number(new_phone)
            driver.set_status(new_status)

            self.driver_service.update_driver(driver)
            print("✅ Driver updated successfully!")
        except Exception as e:
            print(f"❌ Error updating driver: {e}")

    def delete_driver(self):
        try:
            print("\n🗑️ Delete Driver:")
            driver_id = int(input("Enter Driver ID to delete: "))
            self.driver_service.delete_driver(driver_id)
            print(f"✅ Driver with ID {driver_id} deleted successfully!")
        except DriverNotFoundException as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error deleting driver: {e}")

    def view_all_drivers(self):
        try:
            print("\n👨‍✈️ All Drivers:")
            drivers = self.driver_service.get_all_drivers()
            if drivers:
                for driver in drivers:
                    print(f"ID: {driver.get_driver_id()}, Name: {driver.get_name()}, "
                          f"License: {driver.get_license_number()}, Status: {driver.get_status()}")
            else:
                print("❌ No drivers found.")
        except Exception as e:
            print(f"❌ Error fetching drivers: {e}")

    def allocate_driver(self):
        try:
            print("\n🚗 Allocate Driver to Trip:")
            trip_id = int(input("Enter Trip ID: "))
            driver_id = int(input("Enter Driver ID: "))
            
            # Check if driver exists
            driver = self.driver_service.get_driver_by_id(driver_id)
            if not driver:
                print(f"❌ Driver with ID {driver_id} not found.")
                return
                
            # Check if trip exists
            trip = self.trip_service.get_trip_by_id(trip_id)
            if not trip:
                print(f"❌ Trip with ID {trip_id} not found.")
                return
                
            # Check driver availability
            if not self.trip_service.is_driver_available(driver_id):
                print(f"❌ Driver {driver.get_name()} is already assigned to another trip.")
                return
                
            self.trip_service.allocate_driver(trip_id, driver_id)
            print(f"✅ Driver {driver.get_name()} allocated to Trip {trip_id} successfully!")
        except Exception as e:
            print(f"❌ Error allocating driver: {e}")

    def deallocate_driver(self):
        try:
            print("\n🚗 Deallocate Driver:")
            trip_id = int(input("Enter Trip ID: "))
            self.trip_service.deallocate_driver(trip_id)
            print(f"✅ Driver deallocated from Trip {trip_id} successfully!")
        except Exception as e:
            print(f"❌ Error deallocating driver: {e}")