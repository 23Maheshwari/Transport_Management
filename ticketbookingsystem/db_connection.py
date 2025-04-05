import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Ticketbookingsystem"
        )
        if conn.is_connected():
            print("✅ Connection Successful!")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        return None

# Run the connection check
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        conn.close()