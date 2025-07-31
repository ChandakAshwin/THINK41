from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker
from src.models import ProductResponse, DepartmentResponse

# Create database connection (adjust URL based on your database setup)
DATABASE_URL = "sqlite:///./think41.db"  # Using local SQLite database
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Execute the query
query = text("""
    SELECT 
        p.id as product_id,
        p.name as product_name,
        p.category,
        p.brand,
        p.retail_price,
        p.cost,
        p.sku,
        d.name as department_name,
        d.id as department_id
    FROM products p
    INNER JOIN departments d ON p.department_id = d.id
    ORDER BY p.name;
""")

# Execute and print results
results = session.execute(query).all()

print("\nProduct Details with Departments:")
print("-" * 80)
for row in results:
    print(f"Product ID: {row.product_id}")
    print(f"Product Name: {row.product_name}")
    print(f"Category: {row.category}")
    print(f"Brand: {row.brand}")
    print(f"Retail Price: {row.retail_price}")
    print(f"Cost: {row.cost}")
    print(f"SKU: {row.sku}")
    print(f"Department: {row.department_name} (ID: {row.department_id})")
    print("-" * 80)

# Close the session
session.close()
