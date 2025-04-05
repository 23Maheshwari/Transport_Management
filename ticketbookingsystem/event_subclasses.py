import mysql.connector
from abc import ABC, abstractmethod
class Event(ABC):
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
                venue VARCHAR(255) NOT NULL,
                total_seats INT NOT NULL,
                available_seats INT NOT NULL,
                ticket_price DECIMAL(10,2) NOT NULL,
                event_type ENUM('Movie', 'Concert', 'Sport') NOT NULL
            )
        """)
        self.conn.commit()

    @abstractmethod
    def book_tickets(self, event_id, num_tickets):
        pass

    @abstractmethod
    def cancel_booking(self, event_id, num_tickets):
        pass

    @abstractmethod
    def display_event_details(self):
        pass

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
class Movie(Event):
    def book_tickets(self, event_id, num_tickets):
        self.cursor.execute("SELECT available_seats FROM Event WHERE event_id = %s", (event_id,))
        result = self.cursor.fetchone()
        if result and result[0] >= num_tickets:
            new_seats = result[0] - num_tickets
            self.cursor.execute("UPDATE Event SET available_seats = %s WHERE event_id = %s", (new_seats, event_id))
            self.conn.commit()
            print(f"🎥 Successfully booked {num_tickets} Movie tickets!")
        else:
            print("⚠️ Not enough seats available.")

    def cancel_booking(self, event_id, num_tickets):
        self.cursor.execute("SELECT available_seats, total_seats FROM Event WHERE event_id = %s", (event_id,))
        result = self.cursor.fetchone()
        if result:
            new_seats = min(result[0] + num_tickets, result[1])
            self.cursor.execute("UPDATE Event SET available_seats = %s WHERE event_id = %s", (new_seats, event_id))
            self.conn.commit()
            print(f"❌ {num_tickets} Movie tickets canceled successfully!")

    def display_event_details(self):
        self.cursor.execute("SELECT * FROM Event WHERE event_type = 'Movie'")
        movies = self.cursor.fetchall()
        print("\n🎬 Movie Events:")
        for movie in movies:
            print(f"🎟️ {movie[1]} | 📅 {movie[2]} | ⏰ {movie[3]} | 📍 {movie[4]} | 💰 ₹{movie[7]} | Seats: {movie[6]}")


# ✅ Concert Event Subclass
class Concert(Event):
    def book_tickets(self, event_id, num_tickets):
        self.cursor.execute("SELECT available_seats FROM Event WHERE event_id = %s", (event_id,))
        result = self.cursor.fetchone()
        if result and result[0] >= num_tickets:
            new_seats = result[0] - num_tickets
            self.cursor.execute("UPDATE Event SET available_seats = %s WHERE event_id = %s", (new_seats, event_id))
            self.conn.commit()
            print(f"🎶 Successfully booked {num_tickets} Concert tickets!")
        else:
            print("⚠️ Not enough seats available.")

    def cancel_booking(self, event_id, num_tickets):
        self.cursor.execute("SELECT available_seats, total_seats FROM Event WHERE event_id = %s", (event_id,))
        result = self.cursor.fetchone()
        if result:
            new_seats = min(result[0] + num_tickets, result[1])
            self.cursor.execute("UPDATE Event SET available_seats = %s WHERE event_id = %s", (new_seats, event_id))
            self.conn.commit()
            print(f"❌ {num_tickets} Concert tickets canceled successfully!")

    def display_event_details(self):
        self.cursor.execute("SELECT * FROM Event WHERE event_type = 'Concert'")
        concerts = self.cursor.fetchall()
        print("\n🎵 Concert Events:")
        for concert in concerts:
            print(f"🎟️ {concert[1]} | 📅 {concert[2]} | ⏰ {concert[3]} | 📍 {concert[4]} | 💰 ₹{concert[7]} | Seats: {concert[6]}")


# ✅ Sport Event Subclass
class Sport(Event):
    def book_tickets(self, event_id, num_tickets):
        self.cursor.execute("SELECT available_seats FROM Event WHERE event_id = %s", (event_id,))
        result = self.cursor.fetchone()
        if result and result[0] >= num_tickets:
            new_seats = result[0] - num_tickets
            self.cursor.execute("UPDATE Event SET available_seats = %s WHERE event_id = %s", (new_seats, event_id))
            self.conn.commit()
            print(f"🏆 Successfully booked {num_tickets} Sports tickets!")
        else:
            print("⚠️ Not enough seats available.")

    def cancel_booking(self, event_id, num_tickets):
        self.cursor.execute("SELECT available_seats, total_seats FROM Event WHERE event_id = %s", (event_id,))
        result = self.cursor.fetchone()
        if result:
            new_seats = min(result[0] + num_tickets, result[1])
            self.cursor.execute("UPDATE Event SET available_seats = %s WHERE event_id = %s", (new_seats, event_id))
            self.conn.commit()
            print(f"❌ {num_tickets} Sports tickets canceled successfully!")

    def display_event_details(self):
        self.cursor.execute("SELECT * FROM Event WHERE event_type = 'Sport'")
        sports = self.cursor.fetchall()
        print("\n⚽ Sports Events:")
        for sport in sports:
            print(f"🎟️ {sport[1]} | 📅 {sport[2]} | ⏰ {sport[3]} | 📍 {sport[4]} | 💰 ₹{sport[7]} | Seats: {sport[6]}")

if __name__ == "__main__":
    event_type = input("Enter Event Type (Movie/Concert/Sport): ").strip().capitalize()

    if event_type == "Movie":
        event = Movie(host="localhost", user="root", password="yourpassword", database="ticket_db")
    elif event_type == "Concert":
        event = Concert(host="localhost", user="root", password="yourpassword", database="ticket_db")
    elif event_type == "Sport":
        event = Sport(host="localhost", user="root", password="yourpassword", database="ticket_db")
    else:
        print("⚠️ Invalid event type!")
        exit()

    event.display_event_details()
    event_id = int(input("Enter Event ID to Book Tickets: "))
    num_tickets = int(input("Enter Number of Tickets: "))
    event.book_tickets(event_id, num_tickets)
    cancel_id = int(input("Enter Event ID to Cancel Tickets: "))
    cancel_tickets = int(input("Enter Number of Tickets to Cancel: "))
    event.cancel_booking(cancel_id, cancel_tickets)
    event.close_connection()
