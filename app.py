import streamlit as st
import mysql.connector
import pandas as pd
import decimal

# ----------------------------
# MySQL Connection
# ----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sql@krish5",
    database="food_waste_db"
)
cursor = conn.cursor(dictionary=True)

# ----------------------------
# Helper Functions
# ----------------------------
def run_query(query):
    cursor.execute(query)
    result = cursor.fetchall()
    df = pd.DataFrame(result)
    # Convert decimal.Decimal to float
    for col in df.columns:
        df[col] = df[col].apply(lambda x: float(x) if isinstance(x, decimal.Decimal) else x)
    return df

def show_metric(df, col, label):
    if col in df.columns and not df.empty:
        value = df.iloc[0][col]
        if isinstance(value, decimal.Decimal):
            value = float(value)
        st.metric(label, value)

# ----------------------------
# App Layout
# ----------------------------
st.set_page_config(page_title="Food Waste Management Dashboard", layout="wide")
st.title("🍽️ Food Waste Management Dashboard")

# Sidebar Navigation
page = st.sidebar.selectbox("Choose Page", ["Query Dashboard", "CRUD Operations"])

# ----------------------------
# Query Dashboard
# ----------------------------
if page == "Query Dashboard":
    st.header("📊 Query Dashboard")
    
    # Category dropdown
    categories = {
        "Provider Analysis": [
            ("Top 5 Providers by Total Quantity", "SELECT p.Provider_ID, p.Name, SUM(f.Quantity) AS Total_Quantity FROM Providers p JOIN Food_Listings f ON p.Provider_ID = f.Provider_ID GROUP BY p.Provider_ID, p.Name ORDER BY Total_Quantity DESC LIMIT 5"),
            ("Average Quantity by Provider Type", "SELECT Type AS Provider_Type, AVG(f.Quantity) AS Avg_Quantity FROM Providers p JOIN Food_Listings f ON p.Provider_ID = f.Provider_ID GROUP BY Type"),
            ("Cities with Most Active Providers", "SELECT City, COUNT(DISTINCT Provider_ID) AS Num_Providers FROM Providers GROUP BY City ORDER BY Num_Providers DESC"),
            ("Provider with Maximum Claims", "SELECT p.Provider_ID, p.Name, COUNT(c.Claim_ID) AS Total_Claims FROM Providers p JOIN Food_Listings f ON p.Provider_ID = f.Provider_ID JOIN Claims c ON f.Food_ID = c.Food_ID GROUP BY p.Provider_ID, p.Name ORDER BY Total_Claims DESC LIMIT 5"),
            ("Providers Offering Most Vegetarian Food", "SELECT p.Provider_ID, p.Name, COUNT(*) AS Veg_Food_Count FROM Providers p JOIN Food_Listings f ON p.Provider_ID = f.Provider_ID WHERE f.Food_Type='Vegetarian' GROUP BY p.Provider_ID, p.Name ORDER BY Veg_Food_Count DESC")
        ],
        "Receiver Analysis": [
            ("Top 5 Receivers by Total Quantity Claimed", "SELECT r.Receiver_ID, r.Name AS Receiver_Name, SUM(f.Quantity) AS Total_Claimed_Quantity FROM Claims c JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID JOIN Food_Listings f ON c.Food_ID = f.Food_ID GROUP BY r.Receiver_ID, r.Name ORDER BY Total_Claimed_Quantity DESC LIMIT 5"),
            ("Average Quantity Claimed by Receiver Type", "SELECT r.Type AS Receiver_Type, AVG(f.Quantity) AS Avg_Quantity_Claimed FROM Receivers r JOIN Claims c ON r.Receiver_ID = c.Receiver_ID JOIN Food_Listings f ON c.Food_ID = f.Food_ID GROUP BY r.Type"),
            ("Receivers Claiming from Most Providers", "SELECT r.Receiver_ID, r.Name, COUNT(DISTINCT f.Provider_ID) AS Providers_Claimed_From FROM Receivers r JOIN Claims c ON r.Receiver_ID = c.Receiver_ID JOIN Food_Listings f ON c.Food_ID = f.Food_ID GROUP BY r.Receiver_ID, r.Name ORDER BY Providers_Claimed_From DESC LIMIT 5"),
            ("Receivers Claiming More Than 5 Different Food Items", "SELECT r.Receiver_ID, r.Name, COUNT(DISTINCT f.Food_ID) AS Food_Items_Claimed FROM Receivers r JOIN Claims c ON r.Receiver_ID = c.Receiver_ID JOIN Food_Listings f ON c.Food_ID = f.Food_ID GROUP BY r.Receiver_ID, r.Name HAVING Food_Items_Claimed>5 ORDER BY Food_Items_Claimed DESC"),
            ("Average Quantity of Food Claimed per Receiver", "SELECT r.Receiver_ID, r.Name, AVG(f.Quantity) AS Avg_Claimed FROM Claims c JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID JOIN Food_Listings f ON c.Food_ID = f.Food_ID GROUP BY r.Receiver_ID, r.Name ORDER BY Avg_Claimed DESC LIMIT 5")
        ],
        "Food Listings & Availability": [
            ("Total Quantity of Food Available", "SELECT SUM(Quantity) AS Total_Food_Available FROM Food_Listings"),
            ("Top 5 Cities by Food Listings", "SELECT Location AS City, COUNT(*) AS Num_Listings FROM Food_Listings GROUP BY Location ORDER BY Num_Listings DESC LIMIT 5"),
            ("Most Commonly Available Food Types", "SELECT Food_Type, COUNT(*) AS Count_Food_Type FROM Food_Listings GROUP BY Food_Type ORDER BY Count_Food_Type DESC"),
            ("Top 5 Providers Donating Food About to Expire", "SELECT p.Provider_ID, p.Name AS Provider_Name, SUM(f.Quantity) AS Expiring_Quantity FROM Food_Listings f JOIN Providers p ON f.Provider_ID = p.Provider_ID WHERE f.Expiry_Date IS NOT NULL AND f.Expiry_Date <= DATE_ADD(CURDATE(), INTERVAL 7 DAY) GROUP BY p.Provider_ID, p.Name ORDER BY Expiring_Quantity DESC LIMIT 5"),
            ("Average Quantity per Meal Type", "SELECT Meal_Type, AVG(Quantity) AS Avg_Quantity FROM Food_Listings GROUP BY Meal_Type")
        ],
        "Claims & Distribution": [
            ("Number of Claims per Food Item", "SELECT Food_ID, Food_Name, COUNT(*) AS Num_Claims FROM Claims JOIN Food_Listings USING(Food_ID) GROUP BY Food_ID, Food_Name ORDER BY Num_Claims DESC"),
            ("Provider with Highest Successful Claims", "SELECT p.Provider_ID, p.Name, COUNT(c.Claim_ID) AS Successful_Claims FROM Providers p JOIN Food_Listings f ON p.Provider_ID = f.Provider_ID JOIN Claims c ON f.Food_ID = c.Food_ID WHERE c.Status='Completed' GROUP BY p.Provider_ID, p.Name ORDER BY Successful_Claims DESC LIMIT 5"),
            ("Percentage of Claims by Status", "SELECT Status, ROUND(COUNT(*)/(SELECT COUNT(*) FROM Claims)*100,2) AS Percentage FROM Claims GROUP BY Status"),
            ("Most Claimed Meal Type", "SELECT f.Meal_Type, COUNT(*) AS Count_Claimed FROM Claims c JOIN Food_Listings f ON c.Food_ID = f.Food_ID GROUP BY f.Meal_Type ORDER BY Count_Claimed DESC"),
            ("Total Quantity Donated by Each Provider", "SELECT p.Provider_ID, p.Name, SUM(f.Quantity) AS Total_Quantity_Donated FROM Providers p JOIN Food_Listings f ON p.Provider_ID = f.Provider_ID GROUP BY p.Provider_ID, p.Name ORDER BY Total_Quantity_Donated DESC")
        ]
    }

    selected_category = st.selectbox("Select Category", list(categories.keys()))
    if selected_category:
        query_list = [q[0] for q in categories[selected_category]]
        selected_query_name = st.selectbox("Select Query", query_list)
        # Run selected query
        for name, sql in categories[selected_category]:
            if name == selected_query_name:
                df = run_query(sql)
                st.dataframe(df)
                break

# ----------------------------
# CRUD Operations (unchanged)
# ----------------------------
elif page == "CRUD Operations":
    st.header("🛠️ CRUD Operations")
    st.info("Use this section to Add, Update, Delete, or View data for Providers, Receivers, Food Listings, and Claims.")
    
    table = st.selectbox("Select Table", ["Providers","Receivers","Food_Listings","Claims"])
    crud_action = st.radio("Action", ["View", "Add", "Update", "Delete"])
    
    # ---------- View ----------
    if crud_action == "View":
        df = run_query(f"SELECT * FROM {table}")
        st.dataframe(df)
    
    # ---------- Add ----------
    elif crud_action == "Add":
        with st.form("add_form"):
            inputs = {}
            if table=="Providers":
                inputs["Name"] = st.text_input("Name")
                inputs["Type"] = st.text_input("Type")
                inputs["City"] = st.text_input("City")
                inputs["Contact"] = st.text_input("Contact")
            elif table=="Receivers":
                inputs["Name"] = st.text_input("Name")
                inputs["Type"] = st.text_input("Type")
                inputs["City"] = st.text_input("City")
                inputs["Contact"] = st.text_input("Contact")
            elif table=="Food_Listings":
                inputs["Food_Name"] = st.text_input("Food Name")
                inputs["Quantity"] = st.number_input("Quantity", min_value=0)
                inputs["Expiry_Date"] = st.date_input("Expiry Date")
                inputs["Provider_ID"] = st.number_input("Provider ID", min_value=1)
                inputs["Provider_Type"] = st.text_input("Provider Type")
                inputs["Location"] = st.text_input("Location")
                inputs["Food_Type"] = st.text_input("Food Type")
                inputs["Meal_Type"] = st.text_input("Meal Type")
            elif table=="Claims":
                inputs["Food_ID"] = st.number_input("Food ID", min_value=1)
                inputs["Receiver_ID"] = st.number_input("Receiver ID", min_value=1)
                inputs["Status"] = st.text_input("Status")
                inputs["Timestamp"] = st.date_input("Timestamp")
            submitted = st.form_submit_button("Submit")
            if submitted:
                cols = ", ".join(inputs.keys())
                vals = tuple(inputs.values())
                placeholders = ", ".join(["%s"]*len(vals))
                cursor.execute(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})", vals)
                conn.commit()
                st.success(f"{table} added successfully!")

    # ---------- Update ----------
    elif crud_action=="Update":
        id_col = st.text_input("Enter primary key column name (e.g., Provider_ID)")
        id_val = st.number_input("Enter primary key value", min_value=1)
        with st.form("update_form"):
            updates = {}
            if table=="Providers":
                updates["Name"] = st.text_input("New Name")
                updates["Type"] = st.text_input("New Type")
                updates["City"] = st.text_input("New City")
                updates["Contact"] = st.text_input("New Contact")
            elif table=="Receivers":
                updates["Name"] = st.text_input("New Name")
                updates["Type"] = st.text_input("New Type")
                updates["City"] = st.text_input("New City")
                updates["Contact"] = st.text_input("New Contact")
            elif table=="Food_Listings":
                updates["Food_Name"] = st.text_input("Food Name")
                updates["Quantity"] = st.number_input("Quantity", min_value=0)
                updates["Expiry_Date"] = st.date_input("Expiry Date")
                updates["Provider_ID"] = st.number_input("Provider ID", min_value=1)
                updates["Provider_Type"] = st.text_input("Provider Type")
                updates["Location"] = st.text_input("Location")
                updates["Food_Type"] = st.text_input("Food Type")
                updates["Meal_Type"] = st.text_input("Meal Type")
            elif table=="Claims":
                updates["Food_ID"] = st.number_input("Food ID", min_value=1)
                updates["Receiver_ID"] = st.number_input("Receiver ID", min_value=1)
                updates["Status"] = st.text_input("Status")
                updates["Timestamp"] = st.date_input("Timestamp")
            submitted = st.form_submit_button("Update")
            if submitted:
                set_str = ", ".join([f"{k}=%s" for k in updates.keys()])
                vals = tuple(updates.values()) + (id_val,)
                cursor.execute(f"UPDATE {table} SET {set_str} WHERE {id_col}=%s", vals)
                conn.commit()
                st.success(f"{table} updated successfully!")

    # ---------- Delete ----------
    elif crud_action=="Delete":
        id_col = st.text_input("Enter primary key column name (e.g., Provider_ID)")
        id_val = st.number_input("Enter primary key value", min_value=1)
        if st.button("Delete"):
            cursor.execute(f"DELETE FROM {table} WHERE {id_col}=%s", (id_val,))
            conn.commit()
            st.success(f"{table} deleted successfully!")
