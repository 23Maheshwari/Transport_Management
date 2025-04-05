import mysql.connector
from datetime import datetime
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ticketbookingsystem"
)
cursor = db.cursor()

print("\n✅ Connected to MySQL successfully!\n")
def get_venue_id(cursor, venue_name):
    query = "SELECT venue_id FROM Venue WHERE venue_name = %s"
    cursor.execute(query, (venue_name,))
    result = cursor.fetchone()
    return result[0] if result else None
def create_event():
    event_name = input("Enter event name: ")
    event_date = input("Enter event date (YYYY-MM-DD): ")
    event_time = input("Enter event time (HH:MM:SS): ")
    venue_name = input("Enter venue name: ")
    total_seats = int(input("Enter total seats: "))
    ticket_price = float(input("Enter ticket price: "))
    event_type = input("Enter event type (Movie/Sports/Concert): ")

    venue_id = get_venue_id(cursor, venue_name)

    if not venue_id:
        print(f"❌ Error: Venue '{venue_name}' does not exist. Please add it first.")
        return
    query = """
        INSERT INTO Event (event_name, event_date, event_time, venue_id, 
                          total_seats, available_seats, ticket_price, event_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (event_name, event_date, event_time, venue_id, total_seats,
              total_seats, ticket_price, event_type)

    try:
        cursor.execute(query, values)
        db.commit()
        print("✅ Event created successfully!")
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")

def main_menu():
    while True:
        print("\n🎟️ Ticket Booking System Menu 🎟️")
        print("1. Create Event")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_event()
        elif choice == "2":
            print("👋 Exiting Ticket Booking System...")
            break
        else:
            print("❌ Invalid choice. Please try again.")


main_menu()

cursor.close()
db.close()
