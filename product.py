class Product:
    """
    A class to represent a product in the inventory.
    """
    def __init__(self, product_id, name, category, price, stock, gst_percentage=0):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.gst_percentage = gst_percentage

    def update_stock(self, new_stock):
        """Update the stock quantity of the product."""
        self.stock = new_stock

    def update_price(self, new_price):
        """Update the price of the product."""
        self.price = new_price

    def __str__(self):
        """Return a nicely formatted string representation of the product."""
        return (f"Product ID: {self.product_id}\n"
                f"Name: {self.name}\n"
                f"Category: {self.category}\n"
                f"Price: {self.price}\n"
                f"Stock: {self.stock}\n"
                f"GST%: {self.gst_percentage}")
