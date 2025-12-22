import pickle
import sqlite3
import os
from product import Product

class Inventory:
    """
    Manages a collection of Products, with persistence to pickle and sync to SQLite.
    """
    def __init__(self):
        self.products = {}    # Dictionary: product_id -> Product
        self.categories = set()

    def add_product(self, product):
        """Add a new product to the inventory."""
        if product.product_id in self.products:
            print(f"Product with ID {product.product_id} already exists.")
        else:
            self.products[product.product_id] = product
            self.categories.add(product.category)
            print(f"Product {product.product_id} added.")

    def remove_product(self, product_id):
        """Remove a product from the inventory by ID."""
        if product_id in self.products:
            removed = self.products.pop(product_id)
            # Update categories set
            remaining_cats = {p.category for p in self.products.values()}
            if removed.category not in remaining_cats:
                self.categories.discard(removed.category)
            print(f"Product {product_id} removed.")
        else:
            print("Product not found.")

    def update_product(self, product_id, name=None, category=None, price=None, stock=None, gst=None):
        """Update details of an existing product."""
        if product_id not in self.products:
            print("Product not found.")
            return
        prod = self.products[product_id]
        if name:
            prod.name = name
        if category:
            old_cat = prod.category
            prod.category = category
            self.categories.add(category)
            # Remove old category if empty
            if all(p.category != old_cat for p in self.products.values()):
                self.categories.discard(old_cat)
        if price is not None:
            prod.price = price
        if stock is not None:
            prod.stock = stock
        if gst is not None:
            prod.gst_percentage = gst
        print(f"Product {product_id} updated.")

    def search_product(self, key):
        """
        Search for products by ID or name (case-insensitive).
        Returns a list of matching Product objects.
        """
        results = []
        for p in self.products.values():
            if str(p.product_id) == str(key) or p.name.lower() == str(key).lower():
                results.append(p)
        return results

    def list_all_products(self):
        """Print all products in the inventory."""
        if not self.products:
            print("Inventory is empty.")
        for p in self.products.values():
            print(p)
            print("-" * 30)

    def save_to_pickle(self, filename='inventory.pkl'):
        """Save the current inventory dictionary to a pickle file."""
        with open(filename, 'wb') as f:
            pickle.dump(self.products, f)
        print(f"Inventory saved to {filename}.")

    def load_from_pickle(self, filename='inventory.pkl'):
        """Load inventory from a pickle file, if it exists."""
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.products = pickle.load(f)
            self.categories = {p.category for p in self.products.values()}
            print(f"Inventory loaded from {filename}.")
        else:
            print("Pickle file not found.")

    def sync_to_db(self, db_name='inventory.db'):
        """Synchronize the inventory to the SQLite database (products table)."""
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        # Create products table if not exists
        c.execute('''CREATE TABLE IF NOT EXISTS products (
                        product_id INTEGER PRIMARY KEY,
                        name TEXT,
                        category TEXT,
                        price REAL,
                        stock INTEGER
                     )''')
        # Clear and re-insert all products
        c.execute("DELETE FROM products")
        for p in self.products.values():
            c.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)",
                      (p.product_id, p.name, p.category, p.price, p.stock))
        conn.commit()
        conn.close()
        print("Inventory synced to database.")

    def load_from_db(self, db_name='inventory.db'):
        """Load products from the SQLite database into the inventory."""
        if not os.path.exists(db_name):
            print("Database not found.")
            return
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        try:
            c.execute('SELECT product_id, name, category, price, stock FROM products')
            rows = c.fetchall()
        except sqlite3.OperationalError:
            print("Products table does not exist in the database.")
            conn.close()
            return
        self.products = {}
        for row in rows:
            pid, name, cat, price, stock = row
            self.products[pid] = Product(pid, name, cat, price, stock)
        self.categories = {p.category for p in self.products.values()}
        conn.close()
        print("Inventory loaded from database.")
