import mysql.connector


class Venue:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ticketbookingsystem"
        )
        self.cursor = self.conn.cursor()
        self.create_table()  # Ensure table exists

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Venue (
                venue_id INT AUTO_INCREMENT PRIMARY KEY,
                venue_name VARCHAR(255) NOT NULL,
                address TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_venue(self, venue_name, address):
        query = "INSERT INTO Venue (venue_name, address) VALUES (%s, %s)"
        values = (venue_name, address)
        self.cursor.execute(query, values)
        self.conn.commit()
        print("✅ Venue added successfully!")

    def display_venue_details(self):
        self.cursor.execute("SELECT * FROM Venue")
        venues = self.cursor.fetchall()

        if venues:
            print("\n📍 Venue Details:")
            for venue in venues:
                print(f"🏟️ ID: {venue[0]}, Name: {venue[1]}, Address: {venue[2]}")
        else:
            print("⚠️ No venues found in the database.")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    venue_db = Venue(host="localhost", user="root", password="yourpassword", database="ticket_booking")

    while True:
        print("\n🎟️ Venue Management Menu 🎟️")
        print("1. Add Venue")
        print("2. Display Venues")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            venue_name = input("Enter venue name: ")
            address = input("Enter venue address: ")
            venue_db.add_venue(venue_name, address)
        elif choice == "2":
            venue_db.display_venue_details()
        elif choice == "3":
            venue_db.close_connection()
            print("👋 Exiting Venue Management. Have a great day!")
            break
        else:
            print("⚠️ Invalid choice! Please try again.")
