import mysql.connector
from util.db_connection import DBConnUtil

def create_table():
    conn = DBConnUtil.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transport (
            transport_id INT AUTO_INCREMENT PRIMARY KEY,
            vehicle_number VARCHAR(20) NOT NULL,
            vehicle_type VARCHAR(20),
            capacity INT
        );
    """)
    conn.commit()
    print("✅ Transport table created successfully.")
    cursor.close()
    conn.close()

def insert_sample_data():
    conn = DBConnUtil.get_connection()
    cursor = conn.cursor()

    vehicles = [
        ('TN01AB1234', 'Bus', 50),
        ('TN02BC2345', 'Van', 20),
        ('TN03CD3456', 'Mini Bus', 30),
        ('TN04DE4567', 'Bus', 55),
        ('TN05EF5678', 'Van', 25),
        ('TN06FG6789', 'Mini Bus', 35),
        ('TN07GH7890', 'Bus', 60),
        ('TN08HI8901', 'Van', 18),
        ('TN09IJ9012', 'Mini Bus', 40),
        ('TN10JK0123', 'Bus', 52)
    ]

    query = "INSERT INTO transport (vehicle_number, vehicle_type, capacity) VALUES (%s, %s, %s)"
    cursor.executemany(query, vehicles)
    conn.commit()
    print("✅ 10 Transport records inserted successfully.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_table()
    insert_sample_data()
