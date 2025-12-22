import sqlite3
from datetime import datetime

class BillingSystem:
    """
    Handles cart management and billing operations, including saving to the database.
    """
    def __init__(self, inventory):
        self.inventory = inventory
        self.cart = {}   # Dictionary: product_id -> quantity

    def add_to_cart(self, product_id, qty):
        """Add a specified quantity of a product to the cart."""
        if product_id not in self.inventory.products:
            print("Product not found.")
            return
        prod = self.inventory.products[product_id]
        if qty > prod.stock:
            print(f"Only {prod.stock} items available in stock.")
            return
        # Update cart quantities
        self.cart[product_id] = self.cart.get(product_id, 0) + qty
        print(f"Added {qty} of '{prod.name}' to cart.")

    def remove_from_cart(self, product_id):
        """Remove a product entirely from the cart."""
        if product_id in self.cart:
            self.cart.pop(product_id)
            print(f"Removed product {product_id} from cart.")
        else:
            print("Product not in cart.")

    def view_cart(self):
        """Display current items in the cart."""
        if not self.cart:
            print("Cart is empty.")
            return
        print("\nCurrent Cart:")
        for pid, qty in self.cart.items():
            prod = self.inventory.products[pid]
            print(f"{prod.name} (ID: {pid}) - Quantity: {qty}")
        print("")

    def calculate_bill(self):
        """
        Calculate subtotal, total GST, and final total for the current cart.
        Returns a tuple: (subtotal, gst_total, final_total).
        """
        subtotal = 0.0
        gst_total = 0.0
        for pid, qty in self.cart.items():
            prod = self.inventory.products[pid]
            line_total = prod.price * qty
            line_gst = line_total * (prod.gst_percentage / 100)
            subtotal += line_total
            gst_total += line_gst
        final_total = subtotal + gst_total
        return subtotal, gst_total, final_total

    def generate_bill(self):
        """Generate and display the bill, then save it and update inventory."""
        if not self.cart:
            print("Cart is empty. Add items before generating a bill.")
            return
        print("\n============== Customer Bill ================")
        print(f"{'Item':<15}{'Qty':<5}{'Price':<8}{'Total':<8}")
        for pid, qty in self.cart.items():
            prod = self.inventory.products[pid]
            line_total = prod.price * qty
            print(f"{prod.name:<15}{qty:<5}{prod.price:<8}{line_total:<8}")
        subtotal, gst_total, final_total = self.calculate_bill()
        print("\n" + "-"*35)
        print(f"Subtotal: {subtotal:.2f}")
        print(f"GST Total: {gst_total:.2f}")
        print(f"Final Total: {final_total:.2f}")
        print("="*35 + "\n")
        # Save the bill to database
        self.save_bill_to_db()
        # Update inventory stock
        for pid, qty in self.cart.items():
            prod = self.inventory.products[pid]
            prod.stock -= qty
        # Clear the cart
        self.cart.clear()
        # Sync updated stock to DB
        self.inventory.sync_to_db()
        print("Bill generated and inventory updated.")

    def save_bill_to_db(self, db_name='inventory.db'):
        """Save the current bill (cart items) to the SQLite sales table."""
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        # Create sales table if not exists
        c.execute('''CREATE TABLE IF NOT EXISTS sales (
                        bill_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        total_price REAL,
                        date_time TEXT
                     )''')
        # Determine next bill_id
        c.execute("SELECT MAX(bill_id) FROM sales")
        result = c.fetchone()[0]
        next_bill_id = (result or 0) + 1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Insert each cart item as a row in sales
        for pid, qty in self.cart.items():
            prod = self.inventory.products[pid]
            total_price = prod.price * qty
            c.execute("INSERT INTO sales VALUES (?, ?, ?, ?, ?)",
                      (next_bill_id, pid, qty, total_price, now))
        conn.commit()
        conn.close()
        print(f"Bill #{next_bill_id} saved to database.")
