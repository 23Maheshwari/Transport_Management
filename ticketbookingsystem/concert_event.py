import mysql.connector
import pandas as pd
from abc import ABC, abstractmethod

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ticketbookingsystem"
    )
    cursor = conn.cursor(dictionary=True)
    print("✅ Connected to MySQL successfully!")
except mysql.connector.Error as err:
    print(f"❌ Connection Error: {err}")
    exit()
class Event(ABC):
    def __init__(self, event_id, event_name, event_venue, event_date, event_time, ticket_price, event_type, total_seats, available_seats):
        self.event_id = event_id
        self.event_name = event_name
        self.event_venue = event_venue
        self.event_date = event_date
        self.event_time = event_time
        self.ticket_price = ticket_price
        self.event_type = event_type
        self.total_seats = total_seats
        self.available_seats = available_seats

    @abstractmethod
    def display_details(self):
        pass
class Movie(Event):
    def display_details(self):
        return f"🎬 Movie: {self.event_name} at {self.event_venue} on {self.event_date} at {self.event_time} - ₹{self.ticket_price}"

class Concert(Event):
    def display_details(self):
        return f"🎵 Concert: {self.event_name} at {self.event_venue} on {self.event_date} at {self.event_time} - ₹{self.ticket_price}"

class Sport(Event):
    def display_details(self):
        return f"🏆 Sports: {self.event_name} at {self.event_venue} on {self.event_date} at {self.event_time} - ₹{self.ticket_price}"

query = """
SELECT e.event_id, e.event_name, v.venue_name AS event_venue, e.event_date, e.event_time, 
       e.ticket_price, e.event_type, e.total_seats, e.available_seats
FROM Event e
JOIN Venue v ON e.venue_id = v.venue_id;
"""
cursor.execute(query)
events = cursor.fetchall()
event_objects = []
for event in events:
    if event["event_type"] == "Movie":
        event_obj = Movie(**event)
    elif event["event_type"] == "Concert":
        event_obj = Concert(**event)
    elif event["event_type"] == "Sports":
        event_obj = Sport(**event)
    else:
        continue
    event_objects.append(event_obj)
print("\n📌 Loaded Events:")
for event in event_objects:
    print(event.display_details())

cursor.close()
conn.close()
