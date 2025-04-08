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