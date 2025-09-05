import pandas as pd
from pathlib import Path

# ==============================
# Base directory where CSV files are stored
# ==============================
BASE_DIR = Path(r"E:\Desktop\Projects\Food Waste Management")

# Define directories for raw, cleaned, rejected, and report files
RAW_DIR = BASE_DIR
CLEAN_DIR = BASE_DIR / "clean"
REJECT_DIR = BASE_DIR / "rejects"
REPORT_DIR = BASE_DIR / "reports"

# Create output folders if they don’t exist
for folder in [CLEAN_DIR, REJECT_DIR, REPORT_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# ==============================
# Function to clean Providers data
# ==============================
def clean_providers():
    # Read providers CSV
    df = pd.read_csv(RAW_DIR / "providers_data.csv")
    
    # Remove duplicate rows
    df.drop_duplicates(inplace=True)
    
    # Drop rows where Provider_ID or Name is missing
    df.dropna(subset=["Provider_ID", "Name"], inplace=True)
    
    # Convert Provider_ID to integer type
    df["Provider_ID"] = df["Provider_ID"].astype(int)
    
    # Standardize City names (strip whitespace, title case)
    df["City"] = df["City"].astype(str).str.strip().str.title()
    
    # Save cleaned providers data
    df.to_csv(CLEAN_DIR / "providers_data.csv", index=False)
    
    # Print first 5 rows as preview
    print("\n Providers cleaned (first 5 rows):")
    print(df.head())
    
    return df

# ==============================
# Function to clean Receivers data
# ==============================
def clean_receivers():
    df = pd.read_csv(RAW_DIR / "receivers_data.csv")
    df.drop_duplicates(inplace=True)
    df.dropna(subset=["Receiver_ID", "Name"], inplace=True)
    df["Receiver_ID"] = df["Receiver_ID"].astype(int)
    df["City"] = df["City"].astype(str).str.strip().str.title()
    df.to_csv(CLEAN_DIR / "receivers_data.csv", index=False)
    print("\n Receivers cleaned (first 5 rows):")
    print(df.head())
    return df

# ==============================
# Function to clean Food Listings data
# ==============================
def clean_food_listings():
    df = pd.read_csv(RAW_DIR / "food_listings_data.csv")
    df.drop_duplicates(inplace=True)
    df.dropna(subset=["Food_ID", "Food_Name", "Provider_ID"], inplace=True)
    df["Food_ID"] = df["Food_ID"].astype(int)
    df["Provider_ID"] = df["Provider_ID"].astype(int)
    
    # Convert Expiry_Date column to datetime, invalid parsing becomes NaT
    df["Expiry_Date"] = pd.to_datetime(df["Expiry_Date"], errors="coerce")
    
    df.to_csv(CLEAN_DIR / "food_listings_data.csv", index=False)
    print("\n Food Listings cleaned (first 5 rows):")
    print(df.head())
    return df

# ==============================
# Function to clean Claims data
# ==============================
def clean_claims():
    df = pd.read_csv(RAW_DIR / "claims_data.csv")
    df.drop_duplicates(inplace=True)
    df.dropna(subset=["Claim_ID", "Food_ID", "Receiver_ID"], inplace=True)
    df["Claim_ID"] = df["Claim_ID"].astype(int)
    df["Food_ID"] = df["Food_ID"].astype(int)
    df["Receiver_ID"] = df["Receiver_ID"].astype(int)
    
    # Convert Timestamp to datetime, invalid parsing becomes NaT
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    
    df.to_csv(CLEAN_DIR / "claims_data.csv", index=False)
    print("\n Claims cleaned (first 5 rows):")
    print(df.head())
    return df

# ==============================
# Main function to run cleaning and validation
# ==============================
def main():
    print(" Starting data cleaning...")

    # Clean all datasets
    providers = clean_providers()
    receivers = clean_receivers()
    food = clean_food_listings()
    claims = clean_claims()

    # ==============================
    # Validate relationships between datasets
    # ==============================
    # Find claims where Food_ID or Receiver_ID does not exist in master tables
    invalid_claims = claims[
        (~claims["Food_ID"].isin(food["Food_ID"])) |
        (~claims["Receiver_ID"].isin(receivers["Receiver_ID"]))
    ]
    if not invalid_claims.empty:
        invalid_claims.to_csv(REJECT_DIR / "invalid_claims.csv", index=False)
        print(f"\n ErrorFound {len(invalid_claims)} invalid claims (saved to rejects).")

    # Find food listings where Provider_ID does not exist in Providers table
    invalid_food = food[~food["Provider_ID"].isin(providers["Provider_ID"])]
    if not invalid_food.empty:
        invalid_food.to_csv(REJECT_DIR / "invalid_food.csv", index=False)
        print(f"\nError Found {len(invalid_food)} invalid food listings (saved to rejects).")

    # ==============================
    # Generate cleaning report
    # ==============================
    report = {
        "Providers": len(providers),
        "Receivers": len(receivers),
        "Food Listings": len(food),
        "Claims": len(claims),
        "Invalid Claims": len(invalid_claims),
        "Invalid Food": len(invalid_food)
    }
    pd.DataFrame([report]).to_csv(REPORT_DIR / "cleaning_report.csv", index=False)

    # Print report summary
    print("\n Cleaning Report:")
    print(report)
    print("\n Cleaning complete! Check 'clean', 'rejects', and 'reports' folders.")

# ==============================
# Execute main function
# ==============================
if __name__ == "__main__":
    main()
