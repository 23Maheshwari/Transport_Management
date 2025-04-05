from db_connection import get_db_connection
from class_event import Event

class Concert(Event):
    def __init__(self, event_id):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)

                # Fetch Event details (ensuring it's a Concert)
                query = "SELECT event_id, event_name, event_date, event_time, venue_id, total_seats, available_seats, ticket_price FROM event WHERE event_id = %s AND event_type = 'Concert'"
                cursor.execute(query, (event_id,))
                event_data = cursor.fetchone()

                if event_data:
                    # Initialize Parent Class (Event) with Correct Number of Arguments
                    super().__init__(
                        event_data["event_id"], event_data["event_name"], event_data["event_date"],
                        event_data["event_time"], event_data["venue_id"], event_data["total_seats"],
                        event_data["available_seats"], event_data["ticket_price"]
                    )

                    # Fetch Concert Details
                    concert_query = "SELECT artist, type FROM concert WHERE event_id = %s"
                    cursor.execute(concert_query, (event_id,))
                    concert_data = cursor.fetchone()

                    if concert_data:
                        self.artist = concert_data["artist"]
                        self.concert_type = concert_data["type"]
                    else:
                        self.artist = None
                        self.concert_type = None

                else:
                    print(f"❌ No Concert event found for event_id: {event_id}")
                    self.artist = None
                    self.concert_type = None

                cursor.close()
                conn.close()
            except Exception as e:
                print(f"❌ Database Error: {e}")

    def display_concert_details(self):
        """Displays details of the concert event."""
        if hasattr(self, "event_name") and self.event_name:  # Display only if a valid event exists
            super().display_event_details()
            print(f"Artist: {self.artist}")
            print(f"Concert Type: {self.concert_type}")

# Example Usage
if __name__ == "__main__":
    event_id = input("Enter Concert Event ID: ")
    concert = Concert(event_id)
    concert.display_concert_details()
