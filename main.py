from product import Product
from inventory import Inventory
from billing import BillingSystem
from database import initialize_database
from graphs import plot_category_stock, plot_top_selling_products

def main():
    # Initialize inventory and billing system
    inventory = Inventory()
    billing = BillingSystem(inventory)

    # Initialize database tables
    initialize_database()

    while True:
        print("\n==== Inventory & Billing Management System ====")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. View All Products")
        print("5. Search Product")
        print("6. Add Item to Cart")
        print("7. View Cart")
        print("8. Generate Bill")
        print("9. Save Inventory (Pickle)")
        print("10. Load Inventory (Pickle)")
        print("11. Sync Inventory with Database")
        print("12. View Sales Reports (Graphs)")
        print("13. Exit")
        choice = input("Enter your choice (1-13): ")

        if choice == '1':
            # Add Product
            pid = int(input("Enter Product ID: "))
            name = input("Enter Product Name: ")
            category = input("Enter Category: ")
            price = float(input("Enter Price: "))
            stock = int(input("Enter Stock Quantity: "))
            gst = float(input("Enter GST%: "))
            product = Product(pid, name, category, price, stock, gst)
            inventory.add_product(product)

        elif choice == '2':
            # Update Product
            pid = int(input("Enter Product ID to update: "))
            print("Leave blank if not changing a field.")
            name = input("Enter new name: ")
            category = input("Enter new category: ")
            price_input = input("Enter new price: ")
            stock_input = input("Enter new stock quantity: ")
            gst_input = input("Enter new GST%: ")
            # Convert inputs where appropriate
            name = name if name else None
            category = category if category else None
            price = float(price_input) if price_input else None
            stock = int(stock_input) if stock_input else None
            gst = float(gst_input) if gst_input else None
            inventory.update_product(pid, name, category, price, stock, gst)

        elif choice == '3':
            # Delete Product
            pid = int(input("Enter Product ID to delete: "))
            inventory.remove_product(pid)

        elif choice == '4':
            # View All Products
            inventory.list_all_products()

        elif choice == '5':
            # Search Product
            key = input("Enter Product ID or Name to search: ")
            results = inventory.search_product(key)
            if results:
                for prod in results:
                    print(prod)
                    print("-" * 30)
            else:
                print("No matching product found.")

        elif choice == '6':
            # Add Item to Cart
            pid = int(input("Enter Product ID to add to cart: "))
            qty = int(input("Enter quantity: "))
            billing.add_to_cart(pid, qty)

        elif choice == '7':
            # View Cart
            billing.view_cart()

        elif choice == '8':
            # Generate Bill
            billing.generate_bill()

        elif choice == '9':
            # Save Inventory
            inventory.save_to_pickle()

        elif choice == '10':
            # Load Inventory
            inventory.load_from_pickle()

        elif choice == '11':
            # Sync Inventory with Database
            inventory.sync_to_db()

        elif choice == '12':
            # View Sales Reports (Graphs)
            plot_category_stock(inventory)
            plot_top_selling_products()
            print("Graphs have been generated and saved.")

        elif choice == '13':
            # Exit
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
