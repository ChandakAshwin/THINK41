import sqlite3

def run_query():
    # Connect to the database
    conn = sqlite3.connect('database/ecommerce.db')
    cursor = conn.cursor()
    
    # Execute the query
    query = """
    SELECT 
        p.id,
        p.name,
        p.category,
        p.brand,
        p.retail_price,
        p.cost,
        p.sku,
        d.name as department_name,
        d.id as department_id
    FROM products p
    LEFT JOIN departments d ON p.department_id = d.id
    ORDER BY p.name;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Print the results
    print("\nProduct Details with Departments:")
    print("-" * 80)
    for row in results:
        product_id = row[0]
        name = row[1] or "N/A"
        category = row[2] or "N/A"
        brand = row[3] or "N/A"
        retail_price = row[4] or 0
        cost = row[5] or 0
        sku = row[6] or "N/A"
        dept_name = row[7] or "N/A"
        dept_id = row[8]
        
        print(f"Product ID: {product_id}")
        print(f"Product Name: {name}")
        print(f"Category: {category}")
        print(f"Brand: {brand}")
        print(f"Retail Price: ${retail_price:.2f}")
        print(f"Cost: ${cost:.2f}")
        print(f"SKU: {sku}")
        print(f"Department: {dept_name} (ID: {dept_id})")
        print("-" * 80)
    
    # Close the connection
    conn.close()

if __name__ == "__main__":
    run_query()
