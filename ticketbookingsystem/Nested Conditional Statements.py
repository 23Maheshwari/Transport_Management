import mysql.connector
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ticketbookingsystem"
        )
        print("✅ Connected to Database Successfully!")
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None
def get_ticket_price(ticket_type):
    ticket_prices = {
        "Silver": 2000,
        "Gold": 5000,
        "Diamond": 10000
    }

    return ticket_prices.get(ticket_type, None)
def book_tickets(event_id, ticket_type, no_of_booking_tickets):
    conn = get_db_connection()

    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT available_seats FROM event WHERE event_id = %s"
            cursor.execute(query, (event_id,))
            result = cursor.fetchone()

            if result:
                available_tickets = result["available_seats"]
                ticket_price = get_ticket_price(ticket_type)

                if ticket_price is None:
                    print("❌ Invalid Ticket Type! Choose from Silver, Gold, or Diamond.")
                    return
                if available_tickets >= no_of_booking_tickets:
                    total_cost = ticket_price * no_of_booking_tickets
                    remaining_tickets = available_tickets - no_of_booking_tickets
                    update_query = "UPDATE event SET available_seats = %s WHERE event_id = %s"
                    cursor.execute(update_query, (remaining_tickets, event_id))
                    conn.commit()

                    print(f"\n🎟️ {no_of_booking_tickets} {ticket_type} tickets booked successfully!")
                    print(f"💰 Total Cost: ₹{total_cost}")
                    print(f"✅ Remaining Tickets: {remaining_tickets}")
                else:
                    print("❌ Ticket Unavailable! Not enough tickets left.")

            else:
                print("❌ Invalid Event ID! No event found.")

            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print(f"❌ Database Error: {e}")


# Get User Input for Booking
event_id = int(input("Enter Event ID: "))
ticket_type = input("Enter Ticket Type (Silver/Gold/Diamond): ").capitalize()
no_of_booking_tickets = int(input("Enter Number of Tickets to Book: "))

# Call function to book tickets
book_tickets(event_id, ticket_type, no_of_booking_tickets)
