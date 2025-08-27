
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
# products = [
#     ('Laptop', 'SKU1001', 1200.00, 'High performance laptop', 10),
#     ('Smartphone', 'SKU1002', 800.00, 'Latest model smartphone', 15),
#     ('Headphones', 'SKU1003', 150.00, 'Noise cancelling headphones', 30),
#     ('Keyboard', 'SKU1004', 75.00, 'Mechanical keyboard', 20),
#     ('Mouse', 'SKU1005', 50.00, 'Wireless mouse', 25)
# ]

products = [
    # Laptops
    ('Laptop Pro 15', 'SKU2001', 1500.00, 'High performance laptop with 16GB RAM and 512GB SSD', 10),
    ('Laptop Air 13', 'SKU2002', 999.00, 'Lightweight laptop with 8GB RAM and 256GB SSD', 15),
    ('Gaming Laptop X', 'SKU2003', 1800.00, 'Powerful gaming laptop with RTX 3060 GPU', 8),
    ('Business Laptop Elite', 'SKU2004', 1300.00, 'Business-class laptop with extended battery life', 12),
    ('Laptop Basic 14', 'SKU2005', 650.00, 'Budget laptop with 4GB RAM and 128GB SSD', 20),
    ('Ultrabook Slim', 'SKU2006', 1200.00, 'Slim design ultrabook with 512GB SSD', 10),
    ('Laptop Convertible 2-in-1', 'SKU2007', 1100.00, 'Touchscreen convertible laptop', 14),
    ('Laptop Student Edition', 'SKU2008', 500.00, 'Affordable laptop for students', 25),
    ('Laptop Workstation Z', 'SKU2009', 2200.00, 'Workstation laptop for creators', 5),
    ('Laptop Eco Edition', 'SKU2010', 750.00, 'Eco-friendly energy-saving laptop', 18),

    # Smartphones
    ('Smartphone X1', 'SKU3001', 999.00, 'Flagship smartphone with AMOLED display', 20),
    ('Smartphone Lite', 'SKU3002', 450.00, 'Budget smartphone with decent performance', 30),
    ('Smartphone Ultra', 'SKU3003', 1200.00, 'Premium smartphone with 5G and triple camera', 12),
    ('Smartphone Mini', 'SKU3004', 400.00, 'Compact smartphone with good performance', 22),
    ('Smartphone Max', 'SKU3005', 1100.00, 'Large screen smartphone with 6000mAh battery', 15),
    ('Smartphone Fold', 'SKU3006', 1500.00, 'Foldable smartphone with dual screens', 8),
    ('Smartphone Pro Max', 'SKU3007', 1300.00, 'Advanced smartphone with quad camera', 10),
    ('Smartphone 5G Lite', 'SKU3008', 600.00, 'Affordable 5G smartphone', 28),
    ('Smartphone Rugged', 'SKU3009', 700.00, 'Durable smartphone for outdoor use', 12),
    ('Smartphone Student', 'SKU3010', 300.00, 'Budget smartphone for students', 35),

    # Headphones
    ('Headphones NoiseCancel 500', 'SKU4001', 200.00, 'Wireless noise cancelling headphones', 25),
    ('Headphones BassBoost', 'SKU4002', 120.00, 'Deep bass wireless headphones', 30),
    ('Headphones Studio Pro', 'SKU4003', 350.00, 'Professional studio headphones', 12),
    ('Headphones Travel Lite', 'SKU4004', 90.00, 'Lightweight travel headphones', 40),
    ('Headphones Sports', 'SKU4005', 80.00, 'Sweatproof sports headphones', 35),
    ('Headphones Premium 700', 'SKU4006', 250.00, 'Premium sound headphones with mic', 20),
    ('Headphones Classic Wired', 'SKU4007', 60.00, 'Wired headphones with 3.5mm jack', 50),
    ('Headphones Gaming RGB', 'SKU4008', 150.00, 'RGB gaming headphones with surround sound', 22),
    ('Headphones MiniPods', 'SKU4009', 100.00, 'True wireless earbuds', 45),
    ('Headphones Luxury Gold', 'SKU4010', 500.00, 'Luxury limited edition headphones', 5),

    # Shoes
    ('Running Shoes Pro', 'SKU5001', 120.00, 'Lightweight running shoes for athletes', 30),
    ('Casual Sneakers', 'SKU5002', 80.00, 'Everyday casual sneakers', 40),
    ('Leather Formal Shoes', 'SKU5003', 150.00, 'Premium leather formal shoes', 20),
    ('Basketball Shoes', 'SKU5004', 130.00, 'High ankle basketball shoes', 18),
    ('Trail Running Shoes', 'SKU5005', 140.00, 'Durable trail running shoes', 22),
    ('Slip-on Comfort Shoes', 'SKU5006', 60.00, 'Comfort slip-on shoes', 35),
    ('Sneakers Limited Edition', 'SKU5007', 200.00, 'Collector edition sneakers', 10),
    ('Loafers Classic', 'SKU5008', 100.00, 'Classic loafers for daily wear', 25),
    ('Sandals Beachwear', 'SKU5009', 50.00, 'Lightweight sandals for beach', 30),
    ('Sports Shoes Kid', 'SKU5010', 70.00, 'Comfortable sports shoes for kids', 40),

    # Toys
    ('Toy Car', 'SKU6001', 25.00, 'Remote-controlled toy car', 50),
    ('Doll Princess', 'SKU6002', 30.00, 'Beautiful princess doll', 45),
    ('Building Blocks Set', 'SKU6003', 40.00, 'Creative building blocks set', 35),
    ('Puzzle Game', 'SKU6004', 20.00, 'Fun puzzle game for kids', 60),
    ('Action Figure Hero', 'SKU6005', 35.00, 'Superhero action figure', 25),
    ('Toy Train Set', 'SKU6006', 50.00, 'Electric toy train set', 30),
    ('Teddy Bear', 'SKU6007', 28.00, 'Soft and cuddly teddy bear', 55),
    ('Board Game Classic', 'SKU6008', 45.00, 'Classic board game set', 20),
    ('Educational Toy Kit', 'SKU6009', 60.00, 'STEM educational toy kit', 18),
    ('Toy Robot', 'SKU6010', 75.00, 'Interactive toy robot', 15),

    # Chocolates
    ('Dark Chocolate Bar', 'SKU7001', 5.00, '70% cocoa dark chocolate bar', 100),
    ('Milk Chocolate Bar', 'SKU7002', 3.00, 'Creamy milk chocolate bar', 120),
    ('Chocolate Truffle Box', 'SKU7003', 20.00, 'Box of assorted truffles', 50),
    ('Hazelnut Chocolate', 'SKU7004', 8.00, 'Hazelnut filled chocolate', 80),
    ('White Chocolate Bar', 'SKU7005', 4.00, 'Smooth white chocolate bar', 90),
    ('Caramel Chocolate', 'SKU7006', 7.00, 'Caramel filled chocolate', 75),
    ('Chocolate Gift Hamper', 'SKU7007', 50.00, 'Luxury chocolate gift hamper', 20),
    ('Mint Chocolate', 'SKU7008', 6.00, 'Refreshing mint chocolate bar', 70),
    ('Peanut Butter Chocolate', 'SKU7009', 9.00, 'Peanut butter filled chocolate', 60),
    ('Ruby Chocolate', 'SKU7010', 10.00, 'Exotic ruby chocolate bar', 40),
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
