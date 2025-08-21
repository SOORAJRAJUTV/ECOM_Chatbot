# init_db.py
import sqlite3
import datetime

connection = sqlite3.connect("ecom.db")
cursor = connection.cursor()

# Drop tables if they exist (clean start)
cursor.execute("DROP TABLE IF EXISTS order_items;")
cursor.execute("DROP TABLE IF EXISTS orders;")
cursor.execute("DROP TABLE IF EXISTS products;")
cursor.execute("DROP TABLE IF EXISTS customers;")

# Create customers table
cursor.execute("""
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")

# Create products table
cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
)
""")

# Create orders table
cursor.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    status TEXT,
    order_total REAL,
    order_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
)
""")

# Create order_items table
cursor.execute("""
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    qty INTEGER,
    line_total REAL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
""")

# Insert customers
cursor.execute("INSERT INTO customers (name, email) VALUES ('Alice', 'alice@example.com')")
cursor.execute("INSERT INTO customers (name, email) VALUES ('Bob', 'bob@example.com')")

# Insert products
cursor.execute("INSERT INTO products (name, price) VALUES ('T-Shirt', 499)")
cursor.execute("INSERT INTO products (name, price) VALUES ('Hoodie', 1499)")
cursor.execute("INSERT INTO products (name, price) VALUES ('Cap', 299)")

# Insert orders
cursor.execute("INSERT INTO orders (customer_id, status, order_total, order_date) VALUES (1, 'Shipped', 998, ?)", 
               (datetime.datetime.now().strftime("%Y-%m-%d"),))
cursor.execute("INSERT INTO orders (customer_id, status, order_total, order_date) VALUES (2, 'Delivered', 1499, ?)", 
               (datetime.datetime.now().strftime("%Y-%m-%d"),))

# Insert order items
cursor.execute("INSERT INTO order_items (order_id, product_id, qty, line_total) VALUES (1, 1, 2, 998)")
cursor.execute("INSERT INTO order_items (order_id, product_id, qty, line_total) VALUES (2, 2, 1, 1499)")

connection.commit()
connection.close()
print("E-commerce DB initialized successfully!")
