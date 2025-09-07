import sqlite3
import pandas as pd

# Connect to the health_hub database
db_path = "health_hub.db"

try:
    conn = sqlite3.connect(db_path)
    
    # Get all table names
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tables in health_hub.db:")
    for table in tables:
        print(f"- {table[0]}")
    
    print("\n" + "="*50 + "\n")
    
    # Examine each table structure and sample data
    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")
        
        # Get column info
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        print("Columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Get sample data and count
        try:
            count_df = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table_name}", conn)
            print(f"\nTotal rows: {count_df['count'].iloc[0]}")
            
            df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5", conn)
            print(f"Sample data:")
            print(df.to_string())
        except Exception as e:
            print(f"Error reading data: {e}")
        
        print("\n" + "-"*40 + "\n")
    
    conn.close()
    
except Exception as e:
    print(f"Error connecting to database: {e}")