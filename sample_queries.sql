-- Basic SELECT queries

-- 1. Simple SELECT all columns from a table
SELECT * FROM users;

-- 2. Select specific columns
SELECT user_id, username, email FROM users;

-- 3. Using WHERE clause with simple conditions
SELECT * FROM users WHERE age > 18;

-- 4. Multiple conditions with AND/OR
SELECT * FROM users WHERE age > 18 AND is_active = 1;
SELECT * FROM users WHERE age > 18 OR country = 'USA';

-- 5. Using IN operator
SELECT * FROM users WHERE country IN ('USA', 'UK', 'Canada');

-- 6. Using BETWEEN for range queries
SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';

-- 7. Using LIKE for pattern matching
SELECT * FROM products WHERE product_name LIKE '%laptop%';
SELECT * FROM products WHERE product_name LIKE 'L%';

-- 8. Using DISTINCT to get unique values
SELECT DISTINCT country FROM users;

-- 9. ORDER BY for sorting results
SELECT * FROM users ORDER BY last_name ASC;
SELECT * FROM users ORDER BY age DESC;
SELECT * FROM users ORDER BY country, age;

-- 10. LIMIT to restrict number of results
SELECT * FROM users LIMIT 10;
SELECT * FROM users ORDER BY created_at DESC LIMIT 5;

-- 11. Using COUNT, SUM, AVG, MIN, MAX
SELECT COUNT(*) FROM users;
SELECT SUM(order_amount) FROM orders;
SELECT AVG(price) FROM products;
SELECT MIN(salary) FROM employees;
SELECT MAX(salary) FROM employees;

-- 12. GROUP BY with aggregate functions
SELECT country, COUNT(*) as user_count FROM users GROUP BY country;
SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department;

-- 13. HAVING clause with aggregate conditions
SELECT country, COUNT(*) as user_count 
FROM users 
GROUP BY country 
HAVING COUNT(*) > 100;

-- 14. JOIN operations
-- Inner Join
SELECT users.username, orders.order_id 
FROM users 
INNER JOIN orders ON users.user_id = orders.user_id;

-- Left Join
SELECT users.username, orders.order_id 
FROM users 
LEFT JOIN orders ON users.user_id = orders.user_id;

-- Right Join
SELECT users.username, orders.order_id 
FROM users 
RIGHT JOIN orders ON users.user_id = orders.user_id;

-- 15. Subqueries
SELECT * FROM users 
WHERE user_id IN (SELECT user_id FROM orders WHERE order_amount > 1000);

-- 16. CASE statement
SELECT username,
       CASE 
           WHEN age < 18 THEN 'Minor'
           WHEN age BETWEEN 18 AND 60 THEN 'Adult'
           ELSE 'Senior'
       END as age_group
FROM users;

-- 17. Using BETWEEN for time ranges
SELECT * FROM logs 
WHERE log_time BETWEEN '2024-07-01 00:00:00' AND '2024-07-31 23:59:59';

-- 18. Using IS NULL and IS NOT NULL
SELECT * FROM users WHERE email IS NULL;
SELECT * FROM users WHERE email IS NOT NULL;

-- 19. Using EXISTS
SELECT * FROM users 
WHERE EXISTS (SELECT 1 FROM orders WHERE orders.user_id = users.user_id);

-- 20. Using UNION to combine results
SELECT country FROM users 
UNION 
SELECT country FROM suppliers;

-- 21. Using DISTINCT with multiple columns
SELECT DISTINCT country, city FROM users;

-- 22. Using BETWEEN with numbers
SELECT * FROM products 
WHERE price BETWEEN 100 AND 500;

-- 23. Using NOT operator
SELECT * FROM users WHERE NOT is_active = 1;

-- 24. Using IN with subquery
SELECT * FROM products 
WHERE category_id IN (SELECT category_id FROM categories WHERE name IN ('Electronics', 'Computers'));
