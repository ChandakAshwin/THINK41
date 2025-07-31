import pandas as pd
import sqlite3
import os
from pathlib import Path

class EcommerceDataLoader:
    def __init__(self, data_dir="data", db_path="database/ecommerce.db"):
        self.data_dir = Path(data_dir)
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        
    def analyze_csv_structure(self, csv_path):
        """Analyze the structure of the CSV file to understand the data"""
        try:
            df = pd.read_csv(csv_path)
            print(f"CSV Structure Analysis:")
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print(f"Data types:")
            for col, dtype in df.dtypes.items():
                print(f"  {col}: {dtype}")
            print(f"\nFirst few rows:")
            print(df.head())
            print(f"\nMissing values:")
            print(df.isnull().sum())
            return df
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return None
    
    def create_database_table(self, df):
        """Create the database table based on the CSV structure"""
        conn = sqlite3.connect(self.db_path)
        
        # Create products table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            product_name TEXT,
            category TEXT,
            price REAL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        try:
            conn.execute(create_table_sql)
            conn.commit()
            print(f"Database table created successfully at {self.db_path}")
            return True
        except Exception as e:
            print(f"Error creating table: {e}")
            return False
        finally:
            conn.close()
    
    def load_csv_to_database(self, csv_path):
        """Load CSV data into the database"""
        try:
            df = pd.read_csv(csv_path)
            conn = sqlite3.connect(self.db_path)
            
            # Insert data into the table
            df.to_sql('products', conn, if_exists='replace', index=False)
            
            print(f"Successfully loaded {len(df)} records into the database")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
        finally:
            conn.close()
    
    def verify_data_loaded(self):
        """Verify that data was loaded correctly by querying the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get total count
            count_result = conn.execute("SELECT COUNT(*) FROM products").fetchone()
            total_count = count_result[0] if count_result else 0
            
            # Get sample data
            sample_data = conn.execute("SELECT * FROM products LIMIT 5").fetchall()
            
            print(f"Data verification:")
            print(f"Total records in database: {total_count}")
            print(f"Sample data:")
            for row in sample_data:
                print(f"  {row}")
            
            conn.close()
            return total_count > 0
        except Exception as e:
            print(f"Error verifying data: {e}")
            return False
    
    def run_complete_pipeline(self, csv_filename="products.csv"):
        """Run the complete data loading pipeline"""
        csv_path = self.data_dir / csv_filename
        
        if not csv_path.exists():
            print(f"Error: {csv_path} not found!")
            print(f"Please place your {csv_filename} file in the {self.data_dir} directory")
            return False
        
        print("Step 1: Analyzing CSV structure...")
        df = self.analyze_csv_structure(csv_path)
        if df is None:
            return False
        
        print("\nStep 2: Creating database table...")
        if not self.create_database_table(df):
            return False
        
        print("\nStep 3: Loading CSV data into database...")
        if not self.load_csv_to_database(csv_path):
            return False
        
        print("\nStep 4: Verifying data was loaded correctly...")
        if not self.verify_data_loaded():
            return False
        
        print("\n✅ All steps completed successfully!")
        return True

if __name__ == "__main__":
    loader = EcommerceDataLoader()
    loader.run_complete_pipeline() 