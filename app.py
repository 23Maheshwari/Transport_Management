class Passenger:
    def __init__(self, passenger_id, name, age, contact):
        self.passenger_id = passenger_id
        self.name = name
        self.age = age
        self.contact = contact

    def __str__(self):
        return f"[Passenger] ID: {self.passenger_id}, Name: {self.name}, Age: {self.age}, Contact: {self.contact}"


class Trip:
    def __init__(self, trip_id, source, destination, date, status):
        self.trip_id = trip_id
        self.source = source
        self.destination = destination
        self.date = date
        self.status = status

    def __str__(self):
        return f"[Trip] ID: {self.trip_id}, From: {self.source}, To: {self.destination}, Date: {self.date}, Status: {self.status}"


class Booking:
    def __init__(self, booking_id, passenger, trip):
        self.booking_id = booking_id
        self.passenger = passenger
        self.trip = trip

    def __str__(self):
        return f"[Booking] ID: {self.booking_id}\n  {self.passenger}\n  {self.trip}"


# In-memory lists to simulate a database
passengers = []
trips = []
bookings = []

# Admin functionalities
def add_passenger():
    try:
        pid = int(input("Enter Passenger ID: "))
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        contact = input("Enter Contact: ")
        passengers.append(Passenger(pid, name, age, contact))
        print("✅ Passenger added successfully.")
    except:
        print("❌ Invalid input for passenger.")

def add_trip():
    try:
        trip_id = int(input("Enter Trip ID: "))
        source = input("Enter Source: ")
        dest = input("Enter Destination: ")
        date = input("Enter Date (YYYY-MM-DD): ")
        status = input("Enter Status (Scheduled/In Progress/Completed): ")
        trips.append(Trip(trip_id, source, dest, date, status))
        print("✅ Trip added successfully.")
    except:
        print("❌ Invalid input for trip.")

def view_all_data():
    print("\n🧍‍♂️ Passengers:")
    for p in passengers:
        print(p)

    print("\n🗺️ Trips:")
    for tr in trips:
        print(tr)

    print("\n📘 Bookings:")
    for b in bookings:
        print(b)

# Customer functionalities
def book_trip():
    try:
        bid = int(input("Enter Booking ID: "))
        pid = int(input("Enter Passenger ID: "))
        tid = int(input("Enter Trip ID: "))

        passenger = next((p for p in passengers if p.passenger_id == pid), None)
        trip = next((t for t in trips if t.trip_id == tid), None)

        if passenger and trip:
            bookings.append(Booking(bid, passenger, trip))
            print("✅ Booking successful!")
        else:
            print("❌ Invalid Passenger ID or Trip ID.")
    except:
        print("❌ Booking failed. Please check your inputs.")

def view_my_bookings(passenger_id):
    print("\n📘 Your Bookings:")
    for b in bookings:
        if b.passenger.passenger_id == passenger_id:
            print(b)

def customer_menu():
    try:
        pid = int(input("Enter your Passenger ID to log in: "))
        passenger = next((p for p in passengers if p.passenger_id == pid), None)
        if not passenger:
            print("❌ Passenger not found. Please register first.")
            return

        while True:
            print("\n===== Customer Menu =====")
            print("1. Book a Trip")
            print("2. View My Bookings")
            print("3. Logout")
            choice = input("Enter choice: ")

            if choice == "1":
                book_trip()
            elif choice == "2":
                view_my_bookings(pid)
            elif choice == "3":
                print("👋 Logging out. Bye!")
                break
            else:
                print("❌ Invalid choice. Try again.")
    except:
        print("❌ Error in customer menu.")

def admin_menu():
    while True:
        print("\n===== Admin Menu =====")
        print("1. Add Passenger")
        print("2. Add Trip")
        print("3. View All Data")
        print("4. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            add_passenger()
        elif choice == "2":
            add_trip()
        elif choice == "3":
            view_all_data()
        elif choice == "4":
            print("👋 Logging out. Bye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

def main():
    while True:
        print("\n===== Transport Management System =====")
        print("1. Admin Login")
        print("2. Customer Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            admin_menu()
        elif choice == "2":
            customer_menu()
        elif choice == "3":
            print("👋 Exiting system. Bye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()