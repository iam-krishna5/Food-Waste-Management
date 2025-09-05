import mysql.connector
import pandas as pd
from tqdm import tqdm
import os

# ==============================
# MySQL Connection
# ==============================
# Connect to the MySQL server and select the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",       # change if needed
    password="sql@krish5",  # change if needed
    database="food_waste_db"
)
cursor = conn.cursor()  # Create a cursor object to execute SQL queries

# ==============================
# File Paths
# ==============================
# Define paths for clean data and rejected records
clean_path = "clean"
rejects_path = "rejects"
os.makedirs(rejects_path, exist_ok=True)  # Create 'rejects' folder if it doesn't exist

# Read cleaned CSV files into pandas DataFrames
providers = pd.read_csv(os.path.join(clean_path, "providers_data.csv"))
receivers = pd.read_csv(os.path.join(clean_path, "receivers_data.csv"))
food_listings = pd.read_csv(os.path.join(clean_path, "food_listings_data.csv"))
claims = pd.read_csv(os.path.join(clean_path, "claims_data.csv"))

# ==============================
# Helper Function: Insert rows with IGNORE
# ==============================
# This function inserts rows into a table, skips duplicates, and saves rejected rows
def insert_with_ignore(df, query, values_func, reject_file):
    inserted, rejected = 0, 0  # Counters for successful and rejected rows
    rejects = []  # List to store rejected rows

    # Iterate through each row in the DataFrame
    for _, row in tqdm(df.iterrows(), total=len(df)):
        try:
            cursor.execute(query, values_func(row))  # Execute INSERT query
            if cursor.rowcount > 0:  # Row successfully inserted
                inserted += 1
        except Exception as e:
            # Save rejected rows along with the error message
            rejects.append({**row.to_dict(), "Error": str(e)})
            rejected += 1

    conn.commit()  # Commit all inserts

    # Save rejected rows to CSV if any
    if rejects:
        pd.DataFrame(rejects).to_csv(os.path.join(rejects_path, reject_file), index=False)

    return inserted, rejected  # Return counts

# ==============================
# Insert into Providers Table
# ==============================
print("\n Inserting Providers...")
q = """
INSERT IGNORE INTO Providers (Provider_ID, Name, Type, City, Contact)
VALUES (%s, %s, %s, %s, %s)
"""
# Define function to extract values from each row
def provider_vals(r): return (r["Provider_ID"], r["Name"], r["Type"], r["City"], r["Contact"])
ins, rej = insert_with_ignore(providers, q, provider_vals, "providers_rejects.csv")
print(f" Providers: {ins} inserted.  {rej} rejected.")

# ==============================
# Insert into Receivers Table
# ==============================
print("\n Inserting Receivers...")
q = """
INSERT IGNORE INTO Receivers (Receiver_ID, Name, Type, City, Contact)
VALUES (%s, %s, %s, %s, %s)
"""
def receiver_vals(r): return (r["Receiver_ID"], r["Name"], r["Type"], r["City"], r["Contact"])
ins, rej = insert_with_ignore(receivers, q, receiver_vals, "receivers_rejects.csv")
print(f" Receivers: {ins} inserted.  {rej} rejected.")

# ==============================
# Insert into Food Listings Table
# ==============================
print("\n Inserting Food Listings...")
q = """
INSERT IGNORE INTO Food_Listings
(Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
def food_vals(r): 
    return (r["Food_ID"], r["Food_Name"], r["Quantity"], r["Expiry_Date"],
            r["Provider_ID"], r["Provider_Type"], r["Location"], r["Food_Type"], r["Meal_Type"])
ins, rej = insert_with_ignore(food_listings, q, food_vals, "food_listings_rejects.csv")
print(f" Food Listings: {ins} inserted.  {rej} rejected.")

# ==============================
# Insert into Claims Table
# ==============================
print("\n Inserting Claims...")
q = """
INSERT IGNORE INTO Claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp)
VALUES (%s, %s, %s, %s, %s)
"""
def claim_vals(r): return (r["Claim_ID"], r["Food_ID"], r["Receiver_ID"], r["Status"], r["Timestamp"])
ins, rej = insert_with_ignore(claims, q, claim_vals, "claims_rejects.csv")
print(f" Claims: {ins} inserted. {rej} rejected.")

# ==============================
# Final Row Counts
# ==============================
# Function to count rows in a table
def count_rows(table):
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    return cursor.fetchone()[0]

# Print final row counts for verification
print("\n Final Row Counts:")
print(f"Providers: {count_rows('Providers')}")
print(f"Receivers: {count_rows('Receivers')}")
print(f"Food_Listings: {count_rows('Food_Listings')}")
print(f"Claims: {count_rows('Claims')}")

print("\n Import complete with INSERT IGNORE. Reruns won't duplicate data.")
