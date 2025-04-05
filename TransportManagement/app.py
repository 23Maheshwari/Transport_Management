from dao.transport_service import TransportService

class Transport:
    def __init__(self, transport_id, vehicle_number, vehicle_type, capacity):
        self.transport_id = transport_id
        self.vehicle_number = vehicle_number
        self.vehicle_type = vehicle_type
        self.capacity = capacity

    def __str__(self):
        return f"[Transport] ID: {self.transport_id}, Vehicle No: {self.vehicle_number}, Type: {self.vehicle_type}, Capacity: {self.capacity}"


class Passenger:
    def __init__(self, passenger_id, name, age, contact):
        self.passenger_id = passenger_id
        self.name = name
        self.age = age
        self.contact = contact

    def __str__(self):
        return f"[Passenger] ID: {self.passenger_id}, Name: {self.name}, Age: {self.age}, Contact: {self.contact}"


class Trip:
    def __init__(self, trip_id, source, destination, date):
        self.trip_id = trip_id
        self.source = source
        self.destination = destination
        self.date = date

    def __str__(self):
        return f"[Trip] ID: {self.trip_id}, From: {self.source}, To: {self.destination}, Date: {self.date}"


class Booking:
    def __init__(self, booking_id, passenger, trip, transport):
        self.booking_id = booking_id
        self.passenger = passenger
        self.trip = trip
        self.transport = transport

    def __str__(self):
        return f"[Booking] ID: {self.booking_id}\n  {self.passenger}\n  {self.trip}\n  {self.transport}"


# In-memory lists to simulate a database
transports = []
passengers = []
trips = []
bookings = []

def add_transport():
    try:
        tid = int(input("Enter Transport ID: "))
        vno = input("Enter Vehicle Number: ")
        vtype = input("Enter Vehicle Type: ")
        cap = int(input("Enter Capacity: "))
        transports.append(Transport(tid, vno, vtype, cap))
        print("✅ Transport added successfully.")
    except:
        print("❌ Invalid input for transport.")

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
        trips.append(Trip(trip_id, source, dest, date))
        print("✅ Trip added successfully.")
    except:
        print("❌ Invalid input for trip.")

def book_trip():
    try:
        bid = int(input("Enter Booking ID: "))
        pid = int(input("Enter Passenger ID: "))
        tid = int(input("Enter Trip ID: "))
        trans_id = int(input("Enter Transport ID: "))

        passenger = next((p for p in passengers if p.passenger_id == pid), None)
        trip = next((t for t in trips if t.trip_id == tid), None)
        transport = next((tr for tr in transports if tr.transport_id == trans_id), None)

        if passenger and trip and transport:
            bookings.append(Booking(bid, passenger, trip, transport))
            print("✅ Booking successful!")
        else:
            print("❌ Invalid IDs entered.")
    except:
        print("❌ Booking failed. Please check your inputs.")

def view_all():
    print("\n🚍 Transports:")
    for t in transports:
        print(t)

    print("\n🧍‍♂️ Passengers:")
    for p in passengers:
        print(p)

    print("\n🗺️ Trips:")
    for tr in trips:
        print(tr)

    print("\n📘 Bookings:")
    for b in bookings:
        print(b)


def main():
    while True:
        print("\n===== Transport Management System =====")
        print("1. Add Transport")
        print("2. Add Passenger")
        print("3. Add Trip")
        print("4. Book Trip")
        print("5. View All Data")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            add_transport()
        elif choice == "2":
            add_passenger()
        elif choice == "3":
            add_trip()
        elif choice == "4":
            book_trip()
        elif choice == "5":
            view_all()
        elif choice == "6":
            print("👋 Exiting system. Bye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
