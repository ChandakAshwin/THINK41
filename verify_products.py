import sqlite3
import pandas as pd

def verify_products_table():
    """Demonstrate that products have been inserted into the products table"""
    
    # Connect to the database
    conn = sqlite3.connect('database/ecommerce.db')
    
    print("=== PRODUCTS TABLE VERIFICATION ===\n")
    
    # 1. Count total products
    count_query = "SELECT COUNT(*) as total_products FROM products"
    count_result = conn.execute(count_query).fetchone()
    total_products = count_result[0] if count_result else 0
    print(f"1. Total number of products in database: {total_products:,}")
    
    # 2. Show table structure
    print("\n2. Table structure:")
    cursor = conn.execute("PRAGMA table_info(products)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"   - {col[1]} ({col[2]})")
    
    # 3. Show sample products
    print("\n3. Sample products (first 5):")
    sample_query = "SELECT * FROM products LIMIT 5"
    sample_data = pd.read_sql_query(sample_query, conn)
    print(sample_data.to_string(index=False))
    
    # 4. Show products by category
    print("\n4. Products by category:")
    category_query = """
    SELECT category, COUNT(*) as count 
    FROM products 
    GROUP BY category 
    ORDER BY count DESC
    """
    category_data = pd.read_sql_query(category_query, conn)
    print(category_data.to_string(index=False))
    
    # 5. Price statistics (using retail_price instead of price)
    print("\n5. Price statistics:")
    price_query = """
    SELECT 
        MIN(retail_price) as min_price,
        MAX(retail_price) as max_price,
        AVG(retail_price) as avg_price,
        COUNT(*) as total_products
    FROM products
    WHERE retail_price IS NOT NULL
    """
    price_stats = pd.read_sql_query(price_query, conn)
    print(price_stats.to_string(index=False))
    
    # 6. Show some expensive products
    print("\n6. Top 5 most expensive products:")
    expensive_query = """
    SELECT name, category, retail_price 
    FROM products 
    WHERE retail_price IS NOT NULL
    ORDER BY retail_price DESC 
    LIMIT 5
    """
    expensive_data = pd.read_sql_query(expensive_query, conn)
    print(expensive_data.to_string(index=False))
    
    # 7. Show products by brand
    print("\n7. Top 10 brands by product count:")
    brand_query = """
    SELECT brand, COUNT(*) as count 
    FROM products 
    WHERE brand IS NOT NULL
    GROUP BY brand 
    ORDER BY count DESC
    LIMIT 10
    """
    brand_data = pd.read_sql_query(brand_query, conn)
    print(brand_data.to_string(index=False))
    
    # 8. Show cost vs retail price analysis
    print("\n8. Cost vs Retail Price Analysis:")
    cost_analysis_query = """
    SELECT 
        AVG(retail_price - cost) as avg_markup,
        MIN(retail_price - cost) as min_markup,
        MAX(retail_price - cost) as max_markup,
        COUNT(*) as products_with_pricing
    FROM products
    WHERE cost IS NOT NULL AND retail_price IS NOT NULL
    """
    cost_analysis = pd.read_sql_query(cost_analysis_query, conn)
    print(cost_analysis.to_string(index=False))
    
    conn.close()
    
    print(f"\n✅ Verification complete! Found {total_products:,} products in the database.")

if __name__ == "__main__":
    verify_products_table() 