import mysql.connector
import pandas as pd


def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ticketbookingsystem"
        )
        if connection.is_connected():
            print("Connected to MySQL successfully")
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None


def fetch_data(table_name):
    """Fetch all data from a given table."""
    connection = connect_to_mysql()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        df = pd.DataFrame(rows, columns=column_names)

        cursor.close()
        connection.close()

        return df

    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")
        return None
if __name__ == "__main__":
    table_name = "Event"
    event_data = fetch_data(table_name)

    if event_data is not None:
        print(event_data)
    else:
        print("No data found.")
