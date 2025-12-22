import sqlite3
import matplotlib.pyplot as plt

def plot_category_stock(inventory, filename='category_stock.png'):
    """
    Plot a bar chart of available stock by product category.
    """
    # Aggregate stock by category
    category_totals = {}
    for product in inventory.products.values():
        category_totals[product.category] = category_totals.get(product.category, 0) + product.stock
    categories = list(category_totals.keys())
    stocks = list(category_totals.values())

    plt.figure(figsize=(6,4))
    plt.bar(categories, stocks, color=['skyblue','salmon','lightgreen'])
    plt.title('Category-wise Stock Distribution')
    plt.xlabel('Category')
    plt.ylabel('Stock Quantity')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Category-wise stock chart saved as {filename}.")

def plot_top_selling_products(db_name='inventory.db', filename='top_selling.png'):
    """
    Plot a bar chart of top selling products by quantity sold.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # Aggregate total quantity sold per product_id
    query = '''SELECT products.name, SUM(sales.quantity) as total_sold
               FROM sales JOIN products ON sales.product_id = products.product_id
               GROUP BY sales.product_id'''
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    if not rows:
        print("No sales data available to plot.")
        return

    names = [row[0] for row in rows]
    quantities = [row[1] for row in rows]

    plt.figure(figsize=(6,4))
    plt.bar(names, quantities, color=['cyan','orange','lightgreen'])
    plt.title('Top Selling Products')
    plt.xlabel('Product')
    plt.ylabel('Quantity Sold')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Top selling products chart saved as {filename}.")
