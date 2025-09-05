-- Create database
CREATE DATABASE IF NOT EXISTS food_waste_db;
USE food_waste_db;

-- Providers Table
CREATE TABLE IF NOT EXISTS Providers (
    Provider_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(100),
    City VARCHAR(100),
    Contact VARCHAR(100)
);

-- Receivers Table
CREATE TABLE IF NOT EXISTS Receivers (
    Receiver_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(100),
    City VARCHAR(100),
    Contact VARCHAR(100)
);

-- Food Listings Table
CREATE TABLE IF NOT EXISTS Food_Listings (
    Food_ID INT PRIMARY KEY,
    Food_Name VARCHAR(100),
    Quantity INT,
    Expiry_Date DATE,
    Provider_ID INT,
    Provider_Type VARCHAR(100),
    Location VARCHAR(100),
    Food_Type VARCHAR(50),
    Meal_Type VARCHAR(50),
    FOREIGN KEY (Provider_ID) REFERENCES Providers(Provider_ID)
);

-- Claims Table
CREATE TABLE IF NOT EXISTS Claims (
    Claim_ID INT PRIMARY KEY,
    Food_ID INT,
    Receiver_ID INT,
    Status VARCHAR(50),
    Timestamp DATETIME,
    FOREIGN KEY (Food_ID) REFERENCES Food_Listings(Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES Receivers(Receiver_ID)
);





