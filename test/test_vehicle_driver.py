import unittest
from dao.vehicle_dao import VehicleDAO
from entity.vehicle import Vehicle

class TestVehicleDriver(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vehicle_dao = VehicleDAO()
        print("Database connection established for VehicleDAO.")

    def test_add_vehicle_success(self):
        print("\nStarting test: test_add_vehicle_success")
        vehicle = Vehicle(None, 'Ford Transit', 15.00, 'Van', 'Available')
        try:
            self.vehicle_dao.add_vehicle(vehicle)
            print("Vehicle added to database: Ford Transit")

            # Check if the vehicle was added
            self.vehicle_dao.cursor.execute("SELECT * FROM Vehicles WHERE Model = 'Ford Transit'")
            result = self.vehicle_dao.cursor.fetchone()

            if result:
                print(f"Record found in DB: ID={result[0]}, Model={result[1]}, Capacity={result[2]}, Type={result[3]}, Status={result[4]}")
            else:
                print("No record found for 'Ford Transit'.")

            self.assertIsNotNone(result)
            self.assertEqual(result[1], 'Ford Transit')
            self.assertEqual(result[2], 15.00)
            self.assertEqual(result[3], 'Van')
            self.assertEqual(result[4], 'Available')

            print("test_add_vehicle_success passed.")

        except Exception as e:
            print(f"Exception during test_add_vehicle_success: {e}")
            self.fail(f"Test failed due to exception: {e}")

    @classmethod
    def tearDownClass(cls):
        cls.vehicle_dao.conn.close()
        print("Database connection closed for VehicleDAO.")

if __name__ == "__main__":
    unittest.main()
