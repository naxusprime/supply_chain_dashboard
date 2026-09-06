# db_setup.py
import pandas as pd
from sqlalchemy import create_engine

EXCEL_FILE = "Supply chain logisitcs problem.xlsx"
DATABASE_URL = "sqlite:///supply_chain.db"

def init_db():
    engine = create_engine(DATABASE_URL)
    xls = pd.ExcelFile(EXCEL_FILE)
    
    print("Migrating Excel sheets to Database...")
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Clean column names (strip whitespace)
        df.columns = [col.strip() for col in df.columns]
        
        # SQL table name formatting
        table_name = sheet_name.lower()
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"  └─ Migrated sheet: '{sheet_name}' -> Table: '{table_name}' ({len(df)} rows)")
        
    print("\nDatabase initialization complete! Saved as 'supply_chain.db'.")

if __name__ == "__main__":
    init_db()