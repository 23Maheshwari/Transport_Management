import mysql.connector

class Event:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ticketbookingsystem"
        )
        self.cursor = self.conn.cursor()
        self.create_table()
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Event (
                event_id INT AUTO_INCREMENT PRIMARY KEY,
                event_name VARCHAR(255) NOT NULL,
                event_date DATE NOT NULL,
                event_time TIME NOT NULL,
                venue_id INT,
                total_seats INT NOT NULL,
                available_seats INT NOT NULL,
                ticket_price DECIMAL(10,2) NOT NULL,
                event_type ENUM('Movie', 'Sports', 'Concert') NOT NULL,
                FOREIGN KEY (venue_id) REFERENCES Venue(venue_id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    def add_event(self, event_name, event_date, event_time, venue_id, total_seats, ticket_price, event_type):
        query = """
            INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, ticket_price, event_type) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (event_name, event_date, event_time, venue_id, total_seats, total_seats, ticket_price, event_type)
        self.cursor.execute(query, values)
        self.conn.commit()
        print("✅ Event added successfully!")

    def book_tickets(self, event_id, num_tickets):
        self.cursor.execute("SELECT available_seats, ticket_price FROM Event WHERE event_id = %s", (event_id,))
        result = self.cursor.fetchone()

        if result:
            available_seats, ticket_price = result
            if available_seats >= num_tickets:
                new_seats = available_seats - num_tickets
                self.cursor.execute("UPDATE Event SET available_seats = %s WHERE event_id = %s", (new_seats, event_id))
                self.conn.commit()
                total_cost = num_tickets * ticket_price
                print(f"✅ Successfully booked {num_tickets} tickets. Total Cost: ₹{total_cost}")
            else:
                print("⚠️ Not enough seats available!")
        else:
            print("⚠️ Event not found!")

    def cancel_booking(self, event_id, num_tickets):
        self.cursor.execute("SELECT available_seats, total_seats FROM Event WHERE event_id = %s", (event_id,))
        result = self.cursor.fetchone()

        if result:
            available_seats, total_seats = result
            new_seats = available_seats + num_tickets
            if new_seats > total_seats:
                new_seats = total_seats
            self.cursor.execute("UPDATE Event SET available_seats = %s WHERE event_id = %s", (new_seats, event_id))
            self.conn.commit()
            print(f"✅ Successfully canceled {num_tickets} tickets. Seats updated.")
        else:
            print("⚠️ Event not found!")

    def calculate_total_revenue(self, event_id):
        self.cursor.execute("SELECT (total_seats - available_seats) * ticket_price FROM Event WHERE event_id = %s", (event_id,))
        result = self.cursor.fetchone()

        if result and result[0] is not None:
            print(f"💰 Total Revenue: ₹{result[0]}")
            return result[0]
        else:
            print("⚠️ Event not found or no tickets sold!")
            return 0

    def getBookedNoOfTickets(self, event_id):
        self.cursor.execute("SELECT total_seats - available_seats FROM Event WHERE event_id = %s", (event_id,))
        result = self.cursor.fetchone()

        if result and result[0] is not None:
            print(f"🎟️ Total Booked Tickets: {result[0]}")
            return result[0]
        else:
            print("⚠️ No tickets booked for this event.")
            return 0

    def display_event_details(self):
        self.cursor.execute("""
            SELECT e.event_id, e.event_name, e.event_date, e.event_time, v.venue_name, e.total_seats, e.available_seats, e.ticket_price, e.event_type 
            FROM Event e JOIN Venue v ON e.venue_id = v.venue_id
        """)
        events = self.cursor.fetchall()

        if events:
            print("\n📅 Event Details:")
            for event in events:
                print(f"🆔 ID: {event[0]}, 📢 Name: {event[1]}, 📆 Date: {event[2]}, ⏰ Time: {event[3]}")
                print(f"📍 Venue: {event[4]}, 🎟️ Seats: {event[5]}/{event[6]}, 💰 Price: ₹{event[7]}, 🎭 Type: {event[8]}\n")
        else:
            print("⚠️ No events found in the database.")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
if __name__ == "__main__":
    event_db = Event(host="localhost", user="root", password="yourpassword", database="ticket_booking")

    while True:
        print("\n🎭 Event Management Menu 🎭")
        print("1. Add Event")
        print("2. Book Tickets")
        print("3. Cancel Booking")
        print("4. Calculate Total Revenue")
        print("5. Get Booked Tickets")
        print("6. Display Events")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            event_name = input("Enter event name: ")
            event_date = input("Enter event date (YYYY-MM-DD): ")
            event_time = input("Enter event time (HH:MM:SS): ")
            venue_id = input("Enter venue ID: ")
            total_seats = int(input("Enter total seats: "))
            ticket_price = float(input("Enter ticket price: "))
            event_type = input("Enter event type (Movie/Sports/Concert): ")
            event_db.add_event(event_name, event_date, event_time, venue_id, total_seats, ticket_price, event_type)

        elif choice == "2":
            event_id = int(input("Enter event ID: "))
            num_tickets = int(input("Enter number of tickets to book: "))
            event_db.book_tickets(event_id, num_tickets)

        elif choice == "3":
            event_id = int(input("Enter event ID: "))
            num_tickets = int(input("Enter number of tickets to cancel: "))
            event_db.cancel_booking(event_id, num_tickets)

        elif choice == "4":
            event_id = int(input("Enter event ID: "))
            event_db.calculate_total_revenue(event_id)

        elif choice == "5":
            event_id = int(input("Enter event ID: "))
            event_db.getBookedNoOfTickets(event_id)

        elif choice == "6":
            event_db.display_event_details()

        elif choice == "7":
            event_db.close_connection()
            print("👋 Exiting Event Management. Have a great day!")
            break

        else:
            print("⚠️ Invalid choice! Please try again.")
