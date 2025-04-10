from service.admin_service import AdminService

admin_service = AdminService()

class Admin :    
   
    def manage_trips():
        while True:
            print("\n===== Manage Trips =====")
            print("1. Add a New Trip")
            print("2. Update Trip Details")
            print("3. Delete a Trip")
            print("4. View All Trips")
            print("5. Back to Admin Menu")
            choice = input("Enter choice: ")

            if choice == "1":
                admin_service.add_trip()
            elif choice == "2":
                admin_service.update_trip()
            elif choice == "3":
                admin_service.delete_trip()
            elif choice == "4":
                admin_service.view_all_trips()
            elif choice == "5":
                break
            else:
                print("❌ Invalid choice. Try again.")

    def manage_bookings():
        while True:
            print("\n===== Manage Bookings =====")
            print("1. View All Bookings")
            print("2. Cancel a Booking")
            print("3. Delete a Booking")
            print("4. Back to Admin Menu")
            choice = input("Enter choice: ")

            if choice == "1":
                admin_service.view_all_bookings()
            elif choice == "2":
                admin_service.cancel_booking()
            elif choice == "3":
                admin_service.delete_booking()
            elif choice == "4":
                break
            else:
                print("❌ Invalid choice. Try again.")
    
    def manage_passengers():
        while True:
            print("\n===== Manage Passengers =====")
            print("1. View All Passengers")
            print("2. Add a New Passenger")
            print("3. Update Passenger Details")
            print("4. Delete a Passenger")
            print("5. Back to Admin Menu")
            choice = input("Enter choice: ")

            if choice == "1":
                admin_service.view_all_passengers()
            elif choice == "2":
                admin_service.add_passenger()
            elif choice == "3":
                admin_service.update_passenger()
            elif choice == "4":
                admin_service.delete_passenger()
            elif choice == "5":
                break
            else:
                print("❌ Invalid choice. Try again.")
    
    def manage_vehicles():
        while True:
            print("\n===== Manage Vehicles =====")
            print("1. Add a New Vehicle")
            print("2. Update Vehicle Details")
            print("3. Delete a Vehicle")
            print("4. View All Vehicles")
            print("5. Back to Admin Menu")
            choice = input("Enter choice: ")

            if choice == "1":
                admin_service.add_vehicle()
            elif choice == "2":
                admin_service.update_vehicle()
            elif choice == "3":
                admin_service.delete_vehicle()
            elif choice == "4":
                admin_service.view_all_vehicles()
            elif choice == "5":
                break
            else:
                print("❌ Invalid choice. Try again.")
    
    def manage_routes():
        while True:
            print("\n===== Manage Routes =====")
            print("1. Add a New Route")
            print("2. Update Route Details")
            print("3. Delete a Route")
            print("4. View All Routes")
            print("5. Back to Admin Menu")
            choice = input("Enter choice: ")

            if choice == "1":
                admin_service.add_route()
            elif choice == "2":
                admin_service.update_route()
            elif choice == "3":
                admin_service.delete_route()
            elif choice == "4":
                admin_service.view_all_routes()
            elif choice == "5":
                break
            else:
                print("❌ Invalid choice. Try again.")
    
    def view_reports():
        while True:
            print("\n===== Reports and Analytics =====")
            print("1. Booking Statistics")
            print("2. Revenue Reports")
            print("3. Passenger Activity")
            print("4. Trip Utilization")
            print("5. Back to Admin Menu")
            choice = input("Enter choice: ")

            if choice == "1":
                admin_service.view_booking_stats()
            elif choice == "2":
                admin_service.view_revenue_reports()
            elif choice == "3":
                admin_service.view_passenger_activity()
            elif choice == "4":
                admin_service.view_trip_utilization()
            elif choice == "5":
                break
            else:
                print("❌ Invalid choice. Try again.")
    
    def manage_drivers():
        while True:
            print("\n===== Manage Drivers =====")
            print("1. Add New Driver")
            print("2. Update Driver Details")
            print("3. Delete Driver")
            print("4. View All Drivers")
            print("5. Allocate Driver to Trip")
            print("6. Deallocate Driver")
            print("7. Back to Admin Menu")
            choice = input("Enter choice: ")

            if choice == "1":
                admin_service.add_driver()
            elif choice == "2":
                admin_service.update_driver()
            elif choice == "3":
                admin_service.delete_driver()
            elif choice == "4":
                admin_service.view_all_drivers()
            elif choice == "5":
                admin_service.allocate_driver()
            elif choice == "6":
                admin_service.deallocate_driver()
            elif choice == "7":
                break
            else:
                print("❌ Invalid choice. Try again.")