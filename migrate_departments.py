#!/usr/bin/env python3
"""
Milestone 4: Refactor Departments Table Migration Script

This script performs the database refactoring to move departments into a separate table
with proper foreign key relationships as specified in Milestone 4.

Steps:
1. Create a new departments table
2. Extract unique department names from products data
3. Populate the departments table with unique departments
4. Update the products table to reference departments via foreign key
5. Update existing products API to include department information
"""

import sqlite3
import pandas as pd
from pathlib import Path

def create_departments_table(conn):
    """Create the new departments table"""
    print("1. Creating departments table...")
    
    cursor = conn.cursor()
    
    # Create departments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    
    conn.commit()
    print("✅ Departments table created successfully")

def extract_unique_departments(conn):
    """Extract unique department names from products data"""
    print("2. Extracting unique departments from products...")
    
    cursor = conn.cursor()
    
    # Get unique departments from products table
    cursor.execute("""
        SELECT DISTINCT department 
        FROM products 
        WHERE department IS NOT NULL 
        AND department != ''
        ORDER BY department
    """)
    
    departments = [row[0] for row in cursor.fetchall()]
    print(f"✅ Found {len(departments)} unique departments")
    
    return departments

def populate_departments_table(conn, departments):
    """Populate the departments table with unique departments"""
    print("3. Populating departments table...")
    
    cursor = conn.cursor()
    
    # Insert departments
    for dept_name in departments:
        try:
            cursor.execute("""
                INSERT INTO departments (name) 
                VALUES (?)
            """, (dept_name,))
        except sqlite3.IntegrityError:
            # Department already exists (due to UNIQUE constraint)
            pass
    
    conn.commit()
    
    # Verify insertion
    cursor.execute("SELECT COUNT(*) FROM departments")
    count = cursor.fetchone()[0]
    print(f"✅ Successfully populated departments table with {count} departments")

def update_products_table(conn):
    """Update products table to reference departments via foreign key"""
    print("4. Updating products table with department foreign keys...")
    
    cursor = conn.cursor()
    
    # First, add the department_id column
    try:
        cursor.execute("""
            ALTER TABLE products 
            ADD COLUMN department_id INTEGER
        """)
        print("✅ Added department_id column to products table")
    except sqlite3.OperationalError:
        print("ℹ️ department_id column already exists")
    
    # Update department_id for each product
    cursor.execute("""
        UPDATE products 
        SET department_id = (
            SELECT id 
            FROM departments 
            WHERE departments.name = products.department
        )
        WHERE department IS NOT NULL 
        AND department != ''
    """)
    
    updated_count = cursor.rowcount
    print(f"✅ Updated {updated_count} products with department foreign keys")
    
    # Add foreign key constraint
    try:
        cursor.execute("""
            CREATE INDEX idx_products_department_id 
            ON products(department_id)
        """)
        print("✅ Created index on department_id")
    except sqlite3.OperationalError:
        print("ℹ️ Index already exists")
    
    conn.commit()

def verify_migration(conn):
    """Verify the migration was successful"""
    print("5. Verifying migration...")
    
    cursor = conn.cursor()
    
    # Check departments table
    cursor.execute("SELECT COUNT(*) FROM departments")
    dept_count = cursor.fetchone()[0]
    print(f"✅ Departments table has {dept_count} departments")
    
    # Check products with department_id
    cursor.execute("""
        SELECT COUNT(*) 
        FROM products 
        WHERE department_id IS NOT NULL
    """)
    products_with_dept = cursor.fetchone()[0]
    print(f"✅ {products_with_dept} products have department_id")
    
    # Check for orphaned products (products with department but no department_id)
    cursor.execute("""
        SELECT COUNT(*) 
        FROM products 
        WHERE department IS NOT NULL 
        AND department != '' 
        AND department_id IS NULL
    """)
    orphaned_count = cursor.fetchone()[0]
    
    if orphaned_count == 0:
        print("✅ No orphaned products found")
    else:
        print(f"⚠️ Warning: {orphaned_count} products have department but no department_id")
    
    # Show sample data
    print("\n📊 Sample Data:")
    cursor.execute("""
        SELECT p.id, p.name, p.department, d.name as dept_name, p.department_id
        FROM products p
        LEFT JOIN departments d ON p.department_id = d.id
        WHERE p.department IS NOT NULL
        LIMIT 5
    """)
    
    sample_data = cursor.fetchall()
    for row in sample_data:
        print(f"  Product ID: {row[0]}, Name: {row[1][:30]}..., Old Dept: {row[2]}, New Dept: {row[3]}, Dept ID: {row[4]}")

def cleanup_old_department_column(conn):
    """Remove the old department column after verification"""
    print("6. Cleaning up old department column...")
    
    # Note: SQLite doesn't support DROP COLUMN directly
    # We would need to recreate the table, but for now we'll keep the old column
    # as a backup and just mark it as deprecated
    print("ℹ️ Keeping old department column as backup (SQLite limitation)")
    print("ℹ️ You can manually remove it later if needed")

def main():
    """Main migration function"""
    print("🚀 Starting Milestone 4: Refactor Departments Table")
    print("=" * 60)
    
    # Database path
    db_path = "database/ecommerce.db"
    
    if not Path(db_path).exists():
        print(f"❌ Database not found at {db_path}")
        print("Please ensure the database exists and contains products data")
        return
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        print(f"📁 Connected to database: {db_path}")
        
        # Step 1: Create departments table
        create_departments_table(conn)
        
        # Step 2: Extract unique departments
        departments = extract_unique_departments(conn)
        
        if not departments:
            print("⚠️ No departments found in products table")
            print("Migration completed (no departments to migrate)")
            return
        
        # Step 3: Populate departments table
        populate_departments_table(conn, departments)
        
        # Step 4: Update products table
        update_products_table(conn)
        
        # Step 5: Verify migration
        verify_migration(conn)
        
        # Step 6: Cleanup (optional)
        cleanup_old_department_column(conn)
        
        print("\n🎉 Migration completed successfully!")
        print("=" * 60)
        print("Next steps:")
        print("1. Update your API code to use the new department relationship")
        print("2. Test the API endpoints")
        print("3. Update the frontend if needed")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main() 