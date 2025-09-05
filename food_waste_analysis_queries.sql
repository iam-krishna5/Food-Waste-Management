USE food_waste_db;


-- 1) Provider Analysis

-- Query 1: Top 5 Providers by Total Quantity of Food Donated
SELECT Provider_ID, Name, SUM(Quantity) AS Total_Quantity
FROM Food_Listings
JOIN Providers USING(Provider_ID)
GROUP BY Provider_ID, Name
ORDER BY Total_Quantity DESC
LIMIT 5;

-- Query 2: Average Quantity Donated by Each Provider Type
SELECT Type AS Provider_Type, AVG(Quantity) AS Avg_Quantity
FROM Food_Listings
JOIN Providers USING(Provider_ID)
GROUP BY Type;

-- Query 3: Cities with Most Active Providers
SELECT City, COUNT(DISTINCT Provider_ID) AS Num_Providers
FROM Providers
GROUP BY City
ORDER BY Num_Providers DESC;

-- Query 4 : Provider with Maximum Claims on Their Food
SELECT p.Provider_ID, p.Name, COUNT(c.Claim_ID) AS Total_Claims
FROM Providers p
JOIN Food_Listings f ON p.Provider_ID = f.Provider_ID
JOIN Claims c ON f.Food_ID = c.Food_ID
GROUP BY p.Provider_ID, p.Name
ORDER BY Total_Claims DESC
LIMIT 5;

-- Query 5 : Providers Offering Most Vegetarian Food
SELECT p.Provider_ID, p.Name, COUNT(*) AS Veg_Food_Count
FROM Providers p
JOIN Food_Listings f ON p.Provider_ID = f.Provider_ID
WHERE f.Food_Type = 'Vegetarian'
GROUP BY p.Provider_ID, p.Name
ORDER BY Veg_Food_Count DESC;


-- 2) Receiver Analysis

-- Query 6: Top 5 receivers who have claimed the highest total quantity of food
SELECT r.Receiver_ID, r.Name AS Receiver_Name, SUM(f.Quantity) AS Total_Claimed_Quantity
FROM Claims c
JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
JOIN Food_Listings f ON c.Food_ID = f.Food_ID
GROUP BY r.Receiver_ID, r.Name
ORDER BY Total_Claimed_Quantity DESC
LIMIT 5;



-- Query 7: Top 5 Receivers by Total Quantity Claimed
SELECT r.Receiver_ID, r.Name, SUM(f.Quantity) AS Total_Quantity_Claimed
FROM Receivers r
JOIN Claims c ON r.Receiver_ID = c.Receiver_ID
JOIN Food_Listings f ON c.Food_ID = f.Food_ID
GROUP BY r.Receiver_ID, r.Name
ORDER BY Total_Quantity_Claimed DESC
LIMIT 5;

-- Query 8: Average Quantity Claimed by Each Receiver Type
SELECT r.Type AS Receiver_Type, AVG(f.Quantity) AS Avg_Quantity_Claimed
FROM Receivers r
JOIN Claims c ON r.Receiver_ID = c.Receiver_ID
JOIN Food_Listings f ON c.Food_ID = f.Food_ID
GROUP BY r.Type;

-- Query 9 : Receivers Who Claimed Food from Most Providers
SELECT r.Receiver_ID, r.Name, COUNT(DISTINCT f.Provider_ID) AS Providers_Claimed_From
FROM Receivers r
JOIN Claims c ON r.Receiver_ID = c.Receiver_ID
JOIN Food_Listings f ON c.Food_ID = f.Food_ID
GROUP BY r.Receiver_ID, r.Name
ORDER BY Providers_Claimed_From DESC
LIMIT 5;


-- 3) Food Listings & Availability

-- Query 10: Total Quantity of Food Available
SELECT SUM(Quantity) AS Total_Food_Available
FROM Food_Listings;

-- Query 11: City with Highest Number of Food Listings
SELECT Location AS City, COUNT(*) AS Num_Listings
FROM Food_Listings
GROUP BY Location
ORDER BY Num_Listings DESC
LIMIT 5;

-- Query 12: Most Commonly Available Food Types
SELECT Food_Type, COUNT(*) AS Count_Food_Type
FROM Food_Listings
GROUP BY Food_Type
ORDER BY Count_Food_Type DESC;

-- Query 13 : Top 5 providers donating the highest total quantity of food that is about to expire
SELECT p.Provider_ID, p.Name AS Provider_Name, SUM(f.Quantity) AS Expiring_Quantity
FROM Food_Listings f
JOIN Providers p ON f.Provider_ID = p.Provider_ID
WHERE f.Expiry_Date IS NOT NULL
  AND f.Expiry_Date <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)
GROUP BY p.Provider_ID, p.Name
ORDER BY Expiring_Quantity DESC
LIMIT 5;

-- Query 14 : Average Quantity per Meal Type
SELECT Meal_Type, AVG(Quantity) AS Avg_Quantity
FROM Food_Listings
GROUP BY Meal_Type;


-- 4) Claims & Distribution

-- Query 15: Number of Claims per Food Item
SELECT Food_ID, Food_Name, COUNT(*) AS Num_Claims
FROM Claims
JOIN Food_Listings USING(Food_ID)
GROUP BY Food_ID, Food_Name
ORDER BY Num_Claims DESC;

-- Query 16: Provider with Highest Successful Claims
SELECT p.Provider_ID, p.Name, COUNT(c.Claim_ID) AS Successful_Claims
FROM Providers p
JOIN Food_Listings f ON p.Provider_ID = f.Provider_ID
JOIN Claims c ON f.Food_ID = c.Food_ID
WHERE c.Status = 'Completed'
GROUP BY p.Provider_ID, p.Name
ORDER BY Successful_Claims DESC
LIMIT 5;

-- Query 17: Percentage of Claims by Status
SELECT Status, ROUND(COUNT(*) / (SELECT COUNT(*) FROM Claims) * 100, 2) AS Percentage
FROM Claims
GROUP BY Status;

-- Query 18 : Average Quantity of Food Claimed per Receiver
SELECT r.Receiver_ID, r.Name, AVG(f.Quantity) AS Avg_Claimed
FROM Claims c
JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
JOIN Food_Listings f ON c.Food_ID = f.Food_ID
GROUP BY r.Receiver_ID, r.Name
ORDER BY Avg_Claimed DESC
LIMIT 5;

-- Query 19 : Most Claimed Meal Type
SELECT f.Meal_Type, COUNT(*) AS Count_Claimed
FROM Claims c
JOIN Food_Listings f ON c.Food_ID = f.Food_ID
GROUP BY f.Meal_Type
ORDER BY Count_Claimed DESC;

-- Query 20 : Total Quantity Donated by Each Provider
SELECT p.Provider_ID, p.Name, SUM(f.Quantity) AS Total_Quantity_Donated
FROM Providers p
JOIN Food_Listings f ON p.Provider_ID = f.Provider_ID
GROUP BY p.Provider_ID, p.Name
ORDER BY Total_Quantity_Donated DESC;
