import sqlite3
import pandas as pd
from pathlib import Path

# 1. Project directories setup
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "powerco.db"

# 2. Dynamic search function for required CSV files
def find_file(filename):
    target_path = DATA_DIR / filename
    if target_path.exists():
        return target_path
    matches = list(PROJECT_ROOT.rglob(filename))
    if matches:
        return matches[0]
    return None

client_path = find_file("client_data.csv")
price_path = find_file("price_data.csv")

if not client_path:
    raise FileNotFoundError(f"❌ Could not find 'client_data.csv' inside {PROJECT_ROOT} or its subdirectories.")
if not price_path:
    raise FileNotFoundError(f"❌ Could not find 'price_data.csv' inside {PROJECT_ROOT} or its subdirectories.")

print(f"📄 Found client_data at: {client_path}")
print(f"📄 Found price_data at:  {price_path}")

# 3. Read CSV datasets
df_client = pd.read_csv(client_path)
df_price = pd.read_csv(price_path)

# 4. Create SQLite database inside data/powerco.db
print(f"🛠️ Building SQLite database at: {DB_PATH}")
with sqlite3.connect(str(DB_PATH)) as conn:
    df_client.to_sql("client_data", conn, if_exists="replace", index=False)
    df_price.to_sql("price_data", conn, if_exists="replace", index=False)

print(f"✅ Success! Database created at: {DB_PATH}")