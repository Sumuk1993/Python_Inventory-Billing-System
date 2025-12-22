import sqlite3

def initialize_database(db_name='inventory.db'):
    """
    Initialize the SQLite database with products and sales tables.
    This should be called once at the start of the application.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # Create products table
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY,
                    name TEXT,
                    category TEXT,
                    price REAL,
                    stock INTEGER
                 )''')
    # Create sales table
    c.execute('''CREATE TABLE IF NOT EXISTS sales (
                    bill_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER,
                    total_price REAL,
                    date_time TEXT
                 )''')
    conn.commit()
    conn.close()
