-- SQL Optimizer Pro - Test Queries
-- Copy and paste these queries or upload this file to test the application

-- Test Case 1: Basic SELECT with issues
SELECT * FROM users WHERE age > 25 ORDER BY name;

-- Test Case 2: Simple query with functions
SELECT * FROM employees WHERE UPPER(name) = 'JOHN';

-- Test Case 3: Basic JOIN query
SELECT u.name, o.order_date FROM users u JOIN orders o ON u.id = o.user_id;

-- Test Case 4: Multiple JOINs
SELECT u.name, o.order_date, p.name, c.category_name
FROM users u 
JOIN orders o ON u.id = o.user_id 
JOIN order_items oi ON o.id = oi.order_id 
JOIN products p ON oi.product_id = p.id
JOIN categories c ON p.category_id = c.id
WHERE o.order_date > '2024-01-01';

-- Test Case 5: Subquery example
SELECT * FROM users 
WHERE id IN (SELECT user_id FROM orders WHERE total_amount > 1000);

-- Test Case 6: Aggregation query
SELECT category_id, COUNT(*) as product_count, AVG(price) as avg_price
FROM products 
GROUP BY category_id 
ORDER BY product_count DESC;

-- Test Case 7: CROSS JOIN (Performance killer)
SELECT * FROM users CROSS JOIN orders;

-- Test Case 8: Complex WHERE with OR
SELECT * FROM products 
WHERE category_id = 1 OR price > 100 OR name LIKE '%premium%';

-- Test Case 9: Nested subqueries
SELECT * FROM users u 
WHERE u.id IN (
    SELECT o.user_id FROM orders o 
    WHERE o.id IN (
        SELECT oi.order_id FROM order_items oi 
        WHERE oi.product_id IN (
            SELECT p.id FROM products p WHERE p.price > 50
        )
    )
);

-- Test Case 10: Functions in multiple clauses
SELECT UPPER(name) as upper_name, 
       LENGTH(email) as email_length,
       DATE_FORMAT(created_at, '%Y-%m') as month
FROM users 
WHERE LOWER(email) LIKE '%@gmail.com' 
AND YEAR(created_at) = 2024
ORDER BY LENGTH(name) DESC;

-- Test Case 11: Self JOIN
SELECT e1.name as employee, e2.name as manager
FROM employees e1 
JOIN employees e2 ON e1.manager_id = e2.id;

-- Test Case 12: UNION query
SELECT name, email FROM users WHERE age < 25
UNION
SELECT name, email FROM users WHERE age > 65;

-- Test Case 13: Large dataset query
SELECT * FROM sales 
WHERE sale_date BETWEEN '2020-01-01' AND '2024-12-31'
ORDER BY sale_amount DESC;

-- Test Case 14: Complex aggregation
SELECT 
    c.category_name,
    COUNT(p.id) as product_count,
    AVG(p.price) as avg_price,
    MAX(p.price) as max_price,
    MIN(p.price) as min_price,
    SUM(p.stock_quantity) as total_stock
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
GROUP BY c.id, c.category_name
HAVING COUNT(p.id) > 5
ORDER BY avg_price DESC; 