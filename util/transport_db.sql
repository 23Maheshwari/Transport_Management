create database TransportManagement;
use TransportManagement;
CREATE TABLE Vehicles (
    VehicleID INT AUTO_INCREMENT PRIMARY KEY,
    Model VARCHAR(255) NOT NULL,
    Capacity DECIMAL(10, 2) NOT NULL,
    Type VARCHAR(50) CHECK (Type IN ('Truck', 'Van', 'Bus')),
    Status VARCHAR(50) CHECK (Status IN ('Available', 'On Trip', 'Maintenance'))
);
desc vehicles;

CREATE TABLE Routes (
    RouteID INT AUTO_INCREMENT PRIMARY KEY,
    StartDestination VARCHAR(255) NOT NULL,
    EndDestination VARCHAR(255) NOT NULL,
    Distance DECIMAL(10, 2) NOT NULL CHECK (Distance > 0)
);
desc routes;

CREATE TABLE Trips (
    TripID INT AUTO_INCREMENT PRIMARY KEY,
    VehicleID INT NOT NULL,
    RouteID INT NOT NULL,
    DepartureDate DATETIME NOT NULL,
    ArrivalDate DATETIME NOT NULL,
    Status VARCHAR(50) CHECK (Status IN ('Scheduled', 'In Progress', 'Completed', 'Cancelled')),
    TripType VARCHAR(50) DEFAULT 'Freight' CHECK (TripType IN ('Freight', 'Passenger')),
    MaxPassengers INT CHECK (MaxPassengers >= 0),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID) ON DELETE CASCADE,
    FOREIGN KEY (RouteID) REFERENCES Routes(RouteID) ON DELETE CASCADE
);
desc trips;

CREATE TABLE Passengers (
    PassengerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    Gender VARCHAR(255) CHECK (Gender IN ('Male', 'Female', 'Other')),
    Age INT CHECK (Age >= 0),
    Email VARCHAR(255) UNIQUE NOT NULL,
    PhoneNumber VARCHAR(50) NOT NULL
);
desc passengers;

CREATE TABLE Bookings (
    BookingID INT AUTO_INCREMENT PRIMARY KEY,
    TripID INT NOT NULL,
    PassengerID INT NOT NULL,
    BookingDate DATETIME NOT NULL,
    Status VARCHAR(50) CHECK (Status IN ('Confirmed', 'Cancelled', 'Completed')),
    FOREIGN KEY (TripID) REFERENCES Trips(TripID) ON DELETE CASCADE,
    FOREIGN KEY (PassengerID) REFERENCES Passengers(PassengerID) ON DELETE CASCADE
);
desc bookings;

INSERT INTO Vehicles (Model, Capacity, Type, Status) VALUES
('Ford Transit', 15.00, 'Van', 'Available'),
('Mercedes Actros', 30.00, 'Truck', 'On Trip'),
('Volvo Bus', 50.00, 'Bus', 'Maintenance'),
('Scania Truck', 35.00, 'Truck', 'Available'),
('Toyota HiAce', 12.00, 'Van', 'On Trip'),
('MAN Coach', 55.00, 'Bus', 'Available'),
('Iveco Truck', 40.00, 'Truck', 'Maintenance'),
('Isuzu NPR', 25.00, 'Truck', 'Available'),
('Renault Master', 18.00, 'Van', 'On Trip'),
('Setra Bus', 60.00, 'Bus', 'Available');


INSERT INTO Routes (StartDestination, EndDestination, Distance) VALUES
('New York', 'Boston', 350.50),
('Los Angeles', 'San Francisco', 600.75),
('Chicago', 'Houston', 1085.20),
('Miami', 'Orlando', 250.40),
('Dallas', 'Austin', 195.60),
('Seattle', 'Portland', 280.30),
('Denver', 'Las Vegas', 1220.50),
('Atlanta', 'Charlotte', 450.80),
('San Diego', 'Phoenix', 590.40),
('Washington D.C.', 'Philadelphia', 230.90);

INSERT INTO Trips (VehicleID, RouteID, DepartureDate, ArrivalDate, Status, TripType, MaxPassengers) VALUES
(1, 1, '2025-04-01 08:00:00', '2025-04-01 14:00:00', 'Scheduled', 'Passenger', 15),
(2, 2, '2025-04-02 10:00:00', '2025-04-02 18:00:00', 'In Progress', 'Freight', 0),
(3, 3, '2025-04-03 07:30:00', '2025-04-03 21:45:00', 'Completed', 'Passenger', 50),
(4, 4, '2025-04-04 09:00:00', '2025-04-04 13:00:00', 'Scheduled', 'Freight', 0),
(5, 5, '2025-04-05 07:15:00', '2025-04-05 09:30:00', 'Scheduled', 'Passenger', 12),
(6, 6, '2025-04-06 08:00:00', '2025-04-06 12:45:00', 'Scheduled', 'Freight', 0),
(7, 7, '2025-04-07 11:30:00', '2025-04-07 20:30:00', 'Scheduled', 'Passenger', 55),
(8, 8, '2025-04-08 09:45:00', '2025-04-08 16:15:00', 'Completed', 'Passenger', 20),
(9, 9, '2025-04-09 10:30:00', '2025-04-09 17:45:00', 'Cancelled', 'Freight', 0),
(10, 10, '2025-04-10 07:00:00', '2025-04-10 10:45:00', 'Scheduled', 'Passenger', 25);

INSERT INTO Passengers (FirstName, Gender, Age, Email, PhoneNumber) VALUES
('John Doe', 'Male', 28, 'john.doe@example.com', '1234567890'),
('Jane Smith', 'Female', 32, 'jane.smith@example.com', '0987654321'),
('Alex Johnson', 'Other', 25, 'alex.johnson@example.com', '1122334455'),
('Michael Brown', 'Male', 45, 'michael.brown@example.com', '2233445566'),
('Emily Davis', 'Female', 29, 'emily.davis@example.com', '3344556677'),
('Sophia Wilson', 'Female', 36, 'sophia.wilson@example.com', '4455667788'),
('David Martinez', 'Male', 50, 'david.martinez@example.com', '5566778899'),
('Olivia Taylor', 'Female', 22, 'olivia.taylor@example.com', '6677889900'),
('William Anderson', 'Male', 40, 'william.anderson@example.com', '7788990011'),
('Emma Thomas', 'Female', 27, 'emma.thomas@example.com', '8899001122');

INSERT INTO Bookings (TripID, PassengerID, BookingDate, Status) VALUES
(1, 1, '2025-03-25 09:00:00', 'Confirmed'),
(1, 2, '2025-03-25 09:30:00', 'Confirmed'),
(3, 3, '2025-03-26 10:15:00', 'Completed'),
(4, 4, '2025-03-27 08:30:00', 'Cancelled'),
(5, 5, '2025-03-28 07:00:00', 'Confirmed'),
(6, 6, '2025-03-29 10:20:00', 'Confirmed'),
(7, 7, '2025-03-30 08:45:00', 'Confirmed'),
(8, 8, '2025-03-31 07:10:00', 'Completed'),
(9, 9, '2025-04-01 09:25:00', 'Cancelled'),
(10, 10, '2025-04-02 06:50:00', 'Confirmed');

select* from bookings;

CREATE TABLE Drivers (
    DriverID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    LicenseNumber VARCHAR(100) UNIQUE NOT NULL,
    PhoneNumber VARCHAR(50) NOT NULL,
    Status VARCHAR(50) DEFAULT 'Available' CHECK (Status IN ('Available', 'Assigned', 'Inactive'))
);

desc drivers;
INSERT INTO Drivers (Name, LicenseNumber, PhoneNumber, Status) VALUES
('John Smith', 'DL123456789', '9876543210', 'Available'),
('Jane Doe', 'DL987654321', '8765432109', 'Available'),
('Michael Johnson', 'DL456789123', '7654321098', 'Available'),
('Emily Brown', 'DL789123456', '6543210987', 'Available'),
('Sophia Davis', 'DL321654987', '5432109876', 'Available'),
('David Wilson', 'DL654987321', '5432101234', 'Available'),
('Olivia Taylor', 'DL987321654', '4321098765', 'Available'),
('William Anderson', 'DL321987654', '3210987654', 'Available'),
('Emma Thomas', 'DL654123987', '2109876543', 'Available'),
('James Martinez', 'DL987654123', '1098765432', 'Available');

ALTER TABLE Trips
ADD COLUMN DriverID INT,
ADD FOREIGN KEY (DriverID) REFERENCES Drivers(DriverID) ON DELETE SET NULL;