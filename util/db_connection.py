import mysql.connector
from mysql.connector import Error
from util.db_property_util import DBPropertyUtil

class DBConnUtil:
    @staticmethod
    def get_connection():
        try:
            # Load properties from db.properties
            props = DBPropertyUtil.get_connection_string("d:\\Transport_Management\\util\\db.properties")

            # Create connection using loaded properties
            connection = mysql.connector.connect(
                host=props["host"],
                port=int(props["port"]),
                user=props["user"],
                password=props["password"],
                database=props["database"]
            )

            if connection.is_connected():
                print("✅ Database connection successful!")
                return connection

        except Error as e:
            print(f"❌ Error while connecting to DB: {e}")

        return None

# Optional: Test connection when running the script directly
if __name__ == "__main__":
    conn = DBConnUtil.get_connection()
    if conn and conn.is_connected():
        conn.close()
