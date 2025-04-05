import mysql.connector

class Customer:

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
            CREATE TABLE IF NOT EXISTS Customer (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone_number VARCHAR(15) NOT NULL
            )
        """)
        self.conn.commit()

    def add_customer(self, customer_name, email, phone_number):
        try:
            sql = "INSERT INTO Customer (customer_name, email, phone_number) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (customer_name, email, phone_number))
            self.conn.commit()
            print(f"✅ Customer '{customer_name}' added successfully!")
        except mysql.connector.Error as err:
            print(f"⚠️ Error: {err}")

    def get_customer_details(self, customer_id):
        self.cursor.execute("SELECT * FROM Customer WHERE customer_id = %s", (customer_id,))
        customer = self.cursor.fetchone()
        if customer:
            return {
                "Customer ID": customer[0],
                "Name": customer[1],
                "Email": customer[2],
                "Phone Number": customer[3]
            }
        else:
            return "⚠️ Customer not found!"

    def display_customer_details(self, customer_id):
        customer = self.get_customer_details(customer_id)
        if isinstance(customer, dict):
            print("\n👤 Customer Details:")
            for key, value in customer.items():
                print(f"{key}: {value}")
        else:
            print(customer)

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
if __name__ == "__main__":
    customer_db = Customer(host="localhost", user="root", password="yourpassword", database="ticket_db")
    name = input("Enter Customer Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone Number: ")
    customer_db.add_customer(name, email, phone)
    customer_id = int(input("Enter Customer ID to Retrieve Details: "))
    customer_db.display_customer_details(customer_id)
    customer_db.close_connection()
