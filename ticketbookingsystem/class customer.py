import mysql.connector

class Customer:
    def __init__(self, customer_id=None, customer_name=None, email=None, phone_number=None, booking_id=None):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.email = email
        self.phone_number = phone_number
        self.booking_id = booking_id


    def get_customer_name(self):
        return self.customer_name

    def get_email(self):
        return self.email

    def get_phone_number(self):
        return self.phone_number

    def get_booking_id(self):
        return self.booking_id
    def set_customer_name(self, customer_name):
        self.customer_name = customer_name

    def set_email(self, email):
        self.email = email

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

    def set_booking_id(self, booking_id):
        self.booking_id = booking_id
    def display_customer_details(self):
        print(f"Customer ID: {self.customer_id}")
        print(f"Customer Name: {self.customer_name}")
        print(f"Email: {self.email}")
        print(f"Phone Number: {self.phone_number}")
        print(f"Booking ID: {self.booking_id}")
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="TicketBookingSystem"
    )
def fetch_customer(customer_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SHOW COLUMNS FROM Customer")
    columns = [col[0] for col in cursor.fetchall()]

    select_query = f"SELECT {', '.join(columns)} FROM Customer WHERE customer_name = %s"
    cursor.execute(select_query, (customer_name,))

    result = cursor.fetchone()
    conn.close()

    print("Fetched Columns:", columns)
    print("Fetched Data:", result)

    if result:
        if len(result) == 5:
            return Customer(*result)
        else:
            print("Column count mismatch! Adjust Customer class parameters.")
            return None
    else:
        print("Customer not found!")
        return None
customer = fetch_customer("Rohit Sharma")
if customer:
    customer.display_customer_details()
