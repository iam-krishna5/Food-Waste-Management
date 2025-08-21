# 🍽️ Local Food Wastage Management System  

## 📌 Project Overview  
This project aims to **reduce food wastage** by connecting **food providers** (restaurants, grocery stores, catering services) with **food receivers** (NGOs, shelters, individuals). The system manages food listings, claims, and transactions in a structured way using **SQL** and an interactive **Streamlit app**.  

---

## 🎯 Objectives  
- Build a relational database from raw CSV datasets.  
- Clean and validate the data for accuracy and consistency.  
- Enable CRUD operations (Create, Read, Update, Delete).  
- Provide SQL-based insights into food donations and claims.  
- Create an interactive Streamlit dashboard for visualization and user interaction.  

---

## 📂 Dataset Details  
The project uses 4 input datasets (`.csv` files):  
1. **providers_data.csv** → Info about food providers (restaurants, stores, etc.)  
2. **receivers_data.csv** → Info about food receivers (NGOs, shelters, individuals)  
3. **food_listings_data.csv** → Food items listed by providers  
4. **claims_data.csv** → Records of claims made by receivers for available food  

---

## 🛠️ Tech Stack  
- **Python** → Data cleaning, preprocessing, database loading  
- **Pandas** → CSV handling & cleaning  
- **SQL (MySQL/PostgreSQL/SQLite)** → Database schema & queries  
- **Streamlit** → Interactive UI for CRUD and dashboards  
- **Matplotlib / Seaborn** → Data visualizations  

---

## 📑 Project Workflow  
### 🔹 Step 1: Data Cleaning & Validation  
- Removed duplicates & nulls  
- Standardized text formats (city names, food types, etc.)  
- Converted dates and IDs into correct formats  
- Verified foreign key relationships (valid `Provider_ID`, `Receiver_ID`)  
- Output →  
  - `clean/` → cleaned CSVs  
  - `rejects/` → invalid rows (if any)  
  - `reports/cleaning_report.csv` → cleaning summary  

### 🔹 Step 2: Database Setup  
- Designed schema with **4 tables**:  
  - `Providers`  
  - `Receivers`  
  - `Food_Listings`  
  - `Claims`  
- Applied **primary keys** and **foreign keys** to enforce relationships.  

### 🔹 Step 3: Data Loading  
- Loaded cleaned CSVs into the SQL database.  

### 🔹 Step 4: SQL Queries  
- Example queries:  
  - Total claims by status  
  - Food items nearing expiry  
  - Top providers by donations  
  - Top receivers by claims  

### 🔹 Step 5: Streamlit Application  
- Multi-page app with:  
  - 📋 Table views of Providers, Receivers, Food Listings, and Claims  
  - 🔍 Filter/search functionality  
  - ➕ CRUD operations  
  - 📊 Charts for food wastage reduction insights  

---

## 🚀 How to Run the Project  

### 1️⃣ Run Data Cleaning

```bash
cd "E:\Desktop\Projects\Food Waste Management"
python clean_and_validate.py
```
### 2️⃣ Setup Database
Open your SQL client and run the schema script
SOURCE create_tables.sql;

### 3️⃣ Load Data
Load cleaned CSVs into the database
python database_setup.py

### 4️⃣ Run Streamlit App
streamlit run app.py

---
## 📊 Deliverables
-✅ Cleaned datasets (clean/)

-✅ Rejected datasets (rejects/)

-✅ Cleaning report (reports/)

-✅ SQL schema & queries (create_tables.sql, queries.sql)

-✅ Streamlit application (app.py)

---
## 👨‍💻 Author
Krishna Agarwal
