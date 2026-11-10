import sqlite3
import pandas as pd
from pathlib import Path

# Dynamically resolve script and project directories
SCRIPT_DIR = Path(__file__).resolve().parent

# Locate SQL file and DB path regardless of working directory
if (SCRIPT_DIR / "feature_engineering_window_functions.sql").exists():
    sql_file_path = SCRIPT_DIR / "feature_engineering_window_functions.sql"
    db_path = SCRIPT_DIR / "powerco.db" if (SCRIPT_DIR / "powerco.db").exists() else SCRIPT_DIR.parent / "powerco.db"
else:
    sql_file_path = SCRIPT_DIR / "sql" / "feature_engineering_window_functions.sql"
    db_path = SCRIPT_DIR / "powerco.db"

print(f"Connecting to database: {db_path}")
print(f"Loading SQL script: {sql_file_path}")

# Connect to database
conn = sqlite3.connect(str(db_path))

# Read SQL query from file
with open(sql_file_path, 'r') as file:
    sql_script = file.read()

# Execute SQL query directly into pandas DataFrame
engineered_df = pd.read_sql_query(sql_script, conn)

print("\nSQL Feature Engineering successfully executed!")
print(f"Dataset shape: {engineered_df.shape}")
print("\nFirst 5 rows:")
print(engineered_df.head())

conn.close()