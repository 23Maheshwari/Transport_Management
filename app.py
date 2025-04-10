from dao.passenger_dao import PassengerDAO
from dao.booking_dao import BookingDAO
from dao.trip_dao import TripDAO
from service.booking_service import BookingService
from entity.passenger import Passenger
from entity.booking import Booking
from exceptions.exceptions import BookingNotFoundException, InvalidBookingDataException
from admin.admin import Admin
from driver.driver_panel import DriverPanel

# Initialize DAOs and Services
passenger_dao = PassengerDAO()
booking_dao = BookingDAO()
booking_service = BookingService()
trip_dao = TripDAO()

def add_passenger():
    try:
        print("\n📝 Register as a New Customer:")
        name = input("Enter Name: ")
        gender = input("Enter Gender (Male/Female/Other): ").capitalize()
        if gender not in ['Male', 'Female', 'Other']:
            print("❌ Invalid gender. Please enter Male, Female, or Other.")
            return

        try:
            age = int(input("Enter Age: ").strip())
            if age < 0 or age > 120:
                print("❌ Invalid age. Please enter a valid age between 0 and 120.")
                return
        except ValueError:
            print("❌ Invalid input. Age must be a number.")
            return

        email = input("Enter Email: ")
        contact = input("Enter Contact: ")
        if not contact.isdigit() or len(contact) < 10 or len(contact) > 15:
            print("❌ Invalid contact number. It must be numeric and between 10 and 15 digits.")
            return

        passenger = Passenger(None, name, age, contact)
        passenger.set_gender(gender)
        passenger.set_email(email)

        passenger_dao.add_passenger(passenger)
        print("✅ Registration successful!")
    except Exception as e:
        print(f"❌ Error adding passenger: {e}")

def view_all_data():
    try:
        print("\n🧍‍♂️ Registered Passengers:")
        passengers = passenger_dao.get_all_passengers()
        for p in passengers:
            print(p)
    except Exception as e:
        print(f"❌ Error fetching passengers: {e}")

def view_available_trips():
    try:
        print("\n🚌 Available Trips:")
        trips = trip_dao.get_available_trips()
        if trips:
            for trip in trips:
                print(f"TripID: {trip[0]} "
                      f"DepartureDate: {trip[3]}, ArrivalDate: {trip[4]}, , "
                      f"MaxPassengers: {trip[7]}\n\n")
        else:
            print("❌ No trips available at the moment.")
    except Exception as e:
        print(f"❌ Error fetching trips: {e}")

def book_trip():
    try:
        view_available_trips()
        print("\n🚌 Book a Trip:")
        trip_id = int(input("Enter Trip ID: "))
        passenger_id = int(input("Enter Passenger ID: "))
        booking_date = input("Enter Booking Date (YYYY-MM-DD): ")
        status = "Confirmed"

        booking = Booking(None, trip_id, passenger_id, booking_date, status)
        booking_service.book_ticket(booking)
        print("✅ Booking successful!")
    except Exception as e:
        print(f"❌ Error booking trip: {e}")

def view_my_bookings(passenger_id):
    try:
        print("\n📘 Your Latest Booking:")
        booking = booking_service.get_latest_booking_by_passenger_id(passenger_id)
        if booking:
            print(booking)
        else:
            print("❌ No bookings found.")
    except Exception as e:
        print(f"❌ Error fetching bookings: {e}")

def view_past_trips(passenger_id: int):
    try:
        print("\n📚 Your Past Trips:")
        past_trips = booking_service.get_past_bookings_by_passenger_id(passenger_id)
        if past_trips:
            for trip in past_trips:
                print(f"BookingID: {trip[0]}, TripID: {trip[1]}, BookingDate: {trip[3]}, Status: {trip[4]}, "
                      f"DepartureDate: {trip[5]}, ArrivalDate: {trip[6]}, RouteID: {trip[7]}")
        else:
            print("❌ No past trips found.")
    except Exception as e:
        print(f"❌ Error fetching past trips: {e}")

def cancel_booking(passenger_id: int):
    try:
        print("\n🛑 Cancel a Booking:")
        booking_id = int(input("Enter Booking ID to cancel: "))
        booking_service.cancel_booking(booking_id, passenger_id)
        print(f"✅ Booking with ID {booking_id} has been successfully canceled.")
    except BookingNotFoundException as e:
        print(f"❌ {e}")
    except InvalidBookingDataException as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Error canceling booking: {e}")

def customer_menu():
    try:
        print("\n👤 Welcome to Customer Login!")
        is_new_user = input("Are you a new user? (yes/no): ").strip().lower()

        if is_new_user == "yes":
            add_passenger()
            book_now = input("Do you want to book a trip? (yes/no): ").strip().lower()
            if book_now == "yes":
                book_trip()
            return

        elif is_new_user == "no":
            pid = int(input("Enter your Passenger ID to log in: "))
            passenger = passenger_dao.get_passenger_by_id(pid)
            if not passenger:
                print("❌ Passenger not found. Please register first.")
                return

            while True:
                print("\n===== Customer Panel =====")
                print("1. 🚌 Book a Trip")
                print("2. 🛑 Cancel Booking")
                print("3. 📚 View Past Trips")
                print("4. 📘 View Latest Trip")
                print("5. 🚪 Logout")
                choice = input("Enter choice: ")

                if choice == "1":
                    book_trip()
                elif choice == "2":
                    cancel_booking(pid)
                elif choice == "3":
                    view_past_trips(pid)
                elif choice == "4":
                    view_my_bookings(pid)
                elif choice == "5":
                    print("👋 Logging out. Have a nice day!")
                    break
                else:
                    print("❌ Invalid choice. Try again.")
        else:
            print("❌ Invalid input. Please enter 'yes' or 'no'.")
    except Exception as e:
        print(f"❌ Error in customer menu: {e}")

def admin_menu():
    while True:
        print("\n===== Admin Menu =====")
        print("1. Manage Trips")
        print("2. Manage Bookings")
        print("3. Manage Passengers")
        print("4. Manage Vehicles")
        print("5. Manage Routes")
        print("6. Reports and Analytics")
        print("7. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            Admin.manage_trips()
        elif choice == "2":
            Admin.manage_bookings()
        elif choice == "3":
            Admin.manage_passengers()
        elif choice == "4":
            Admin.manage_vehicles()
        elif choice == "5":
            Admin.manage_routes()
        elif choice == "6":
            Admin.view_reports()
        elif choice == "7":
            print("👋 Logging out. Bye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

def driver_menu():
    try:
        print("\n🚚 Welcome to Driver Login")
        driver_id = int(input("Enter your Driver ID: "))
        driver_panel = DriverPanel(driver_id)
        driver_panel.show_menu()
    except Exception as e:
        print(f"❌ Error in driver menu: {e}")

def main():
    while True:
        print("\n===== Transport Management System =====")
        print("1. 👨‍💼 Admin Login")
        print("2. 👤 Customer Login")
        print("3. 🚚 Driver Login")
        print("4. 🚪 Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            admin_menu()
        elif choice == "2":
            customer_menu()
        elif choice == "3":
            driver_menu()
        elif choice == "4":
            print("👋 Exiting system. Bye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
