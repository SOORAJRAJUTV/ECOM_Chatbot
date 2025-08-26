
# init_db.py
import sqlite3
import datetime

connection = sqlite3.connect("ecom.db")
cursor = connection.cursor()

# Drop tables if they exist (clean start)
cursor.execute("DROP TABLE IF EXISTS order_items;")
cursor.execute("DROP TABLE IF EXISTS orders;")
cursor.execute("DROP TABLE IF EXISTS products;")
cursor.execute("DROP TABLE IF EXISTS addresses;")
cursor.execute("DROP TABLE IF EXISTS users;")

# Create users table
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE NOT NULL,
    account_number TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# Create addresses table
cursor.execute("""
CREATE TABLE addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT CHECK(type IN ('billing','shipping')) NOT NULL,
    first_name TEXT,
    last_name TEXT,
    company TEXT,
    address1 TEXT NOT NULL,
    address2 TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL,
    country TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# Create products table
cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    sku TEXT UNIQUE,
    price REAL NOT NULL,
    description TEXT,
    stock INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# Create orders table
cursor.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('Pending','Confirmed','Shipped','Delivered','Cancelled')) DEFAULT 'Pending',
    order_number TEXT UNIQUE,
    billing_address_id INTEGER,
    shipping_address_id INTEGER,
    payment_method TEXT,
    tracking_number TEXT,
    subtotal REAL,
    tax REAL,
    shipping_cost REAL,
    total REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(billing_address_id) REFERENCES addresses(id),
    FOREIGN KEY(shipping_address_id) REFERENCES addresses(id)
)
""")

# Create order_items table
cursor.execute("""
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    qty INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    line_total REAL NOT NULL,
    tracking_number TEXT,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
""")

# Insert users
users = [
    ('John', 'Doe', '1234567890', 'john.doe@example.com', 'ACC1001'),
    ('Jane', 'Smith', '9876543210', 'jane.smith@example.com', 'ACC1002'),
    ('Michael', 'Brown', '5551234567', 'michael.brown@example.com', 'ACC1003'),
    ('Emily', 'Davis', '4449876543', 'emily.davis@example.com', 'ACC1004'),
    ('David', 'Wilson', '2223334444', 'david.wilson@example.com', 'ACC1005')
]
cursor.executemany("INSERT INTO users (first_name, last_name, phone, email, account_number) VALUES (?, ?, ?, ?, ?)", users)

# Insert addresses
addresses = [
    (1, 'billing', 'John', 'Doe', 'JD Corp', '123 Main St', 'Apt 4B', 'New York', 'NY', '10001', 'USA', '1234567890', 'john.doe@example.com'),
    (1, 'shipping', 'John', 'Doe', None, '456 Oak St', None, 'Brooklyn', 'NY', '11201', 'USA', '1234567890', 'john.doe@example.com'),
    (2, 'billing', 'Jane', 'Smith', 'Smith LLC', '789 Pine St', None, 'San Francisco', 'CA', '94105', 'USA', '9876543210', 'jane.smith@example.com'),
    (3, 'shipping', 'Michael', 'Brown', None, '321 Elm St', 'Suite 200', 'Chicago', 'IL', '60601', 'USA', '5551234567', 'michael.brown@example.com'),
    (4, 'billing', 'Emily', 'Davis', 'ED Solutions', '654 Maple Ave', None, 'Seattle', 'WA', '98101', 'USA', '4449876543', 'emily.davis@example.com')
]
cursor.executemany("""INSERT INTO addresses 
(user_id, type, first_name, last_name, company, address1, address2, city, state, zip, country, phone, email) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", addresses)

# Insert products
products = [
    ('Laptop', 'SKU1001', 1200.00, 'High performance laptop', 10),
    ('Smartphone', 'SKU1002', 800.00, 'Latest model smartphone', 15),
    ('Headphones', 'SKU1003', 150.00, 'Noise cancelling headphones', 30),
    ('Keyboard', 'SKU1004', 75.00, 'Mechanical keyboard', 20),
    ('Mouse', 'SKU1005', 50.00, 'Wireless mouse', 25)
]
cursor.executemany("INSERT INTO products (name, sku, price, description, stock) VALUES (?, ?, ?, ?, ?)", products)

# Insert orders
orders = [
    (1, 'Pending', 'ORD1001', 1, 2, 'Credit Card', 'TRK1001', 1250.00, 100.00, 20.00, 1370.00),
    (2, 'Confirmed', 'ORD1002', 3, 3, 'PayPal', 'TRK1002', 800.00, 64.00, 15.00, 879.00),
    (3, 'Shipped', 'ORD1003', 4, 4, 'Debit Card', 'TRK1003', 225.00, 18.00, 10.00, 253.00),
    (4, 'Delivered', 'ORD1004', 5, 5, 'Credit Card', 'TRK1004', 75.00, 6.00, 5.00, 86.00),
    (5, 'Cancelled', 'ORD1005', 1, 2, 'Net Banking', 'TRK1005', 50.00, 4.00, 5.00, 59.00)
]
cursor.executemany("""INSERT INTO orders 
(user_id, status, order_number, billing_address_id, shipping_address_id, payment_method, tracking_number, subtotal, tax, shipping_cost, total) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", orders)

# Insert order items
order_items = [
    (1, 1, 1, 1200.00, 1200.00, 'TRK1001'),
    (1, 5, 1, 50.00, 50.00, 'TRK1001'),
    (2, 2, 1, 800.00, 800.00, 'TRK1002'),
    (3, 3, 1, 150.00, 150.00, 'TRK1003'),
    (3, 4, 1, 75.00, 75.00, 'TRK1003'),
    (4, 4, 1, 75.00, 75.00, 'TRK1004'),
    (5, 5, 1, 50.00, 50.00, 'TRK1005')
]
cursor.executemany("INSERT INTO order_items (order_id, product_id, qty, unit_price, line_total, tracking_number) VALUES (?, ?, ?, ?, ?, ?)", order_items)

connection.commit()
connection.close()
print("E-commerce DB (users, addresses, products, orders, order_items) initialized successfully!")




































# # init_db.py
# import sqlite3
# import datetime

# connection = sqlite3.connect("ecom.db")
# cursor = connection.cursor()

# # Drop tables if they exist (clean start)
# cursor.execute("DROP TABLE IF EXISTS order_items;")
# cursor.execute("DROP TABLE IF EXISTS orders;")
# cursor.execute("DROP TABLE IF EXISTS products;")
# cursor.execute("DROP TABLE IF EXISTS customers;")

# # Create customers table
# cursor.execute("""
# CREATE TABLE customers (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT UNIQUE NOT NULL
# )
# """)

# # Create products table
# cursor.execute("""
# CREATE TABLE products (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     price REAL NOT NULL
# )
# """)

# # Create orders table
# cursor.execute("""
# CREATE TABLE orders (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     customer_id INTEGER,
#     status TEXT,
#     order_total REAL,
#     order_date TEXT,
#     FOREIGN KEY(customer_id) REFERENCES customers(id)
# )
# """)

# # Create order_items table
# cursor.execute("""
# CREATE TABLE order_items (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     order_id INTEGER,
#     product_id INTEGER,
#     qty INTEGER,
#     line_total REAL,
#     FOREIGN KEY(order_id) REFERENCES orders(id),
#     FOREIGN KEY(product_id) REFERENCES products(id)
# )
# """)

# # Insert customers
# cursor.execute("INSERT INTO customers (name, email) VALUES ('Alice', 'alice@example.com')")
# cursor.execute("INSERT INTO customers (name, email) VALUES ('Bob', 'bob@example.com')")

# # Insert products
# cursor.execute("INSERT INTO products (name, price) VALUES ('T-Shirt', 499)")
# cursor.execute("INSERT INTO products (name, price) VALUES ('Hoodie', 1499)")
# cursor.execute("INSERT INTO products (name, price) VALUES ('Cap', 299)")

# # Insert orders
# cursor.execute("INSERT INTO orders (customer_id, status, order_total, order_date) VALUES (1, 'Shipped', 998, ?)", 
#                (datetime.datetime.now().strftime("%Y-%m-%d"),))
# cursor.execute("INSERT INTO orders (customer_id, status, order_total, order_date) VALUES (2, 'Delivered', 1499, ?)", 
#                (datetime.datetime.now().strftime("%Y-%m-%d"),))

# # Insert order items
# cursor.execute("INSERT INTO order_items (order_id, product_id, qty, line_total) VALUES (1, 1, 2, 998)")
# cursor.execute("INSERT INTO order_items (order_id, product_id, qty, line_total) VALUES (2, 2, 1, 1499)")

# connection.commit()
# connection.close()
# print("E-commerce DB initialized successfully!")
