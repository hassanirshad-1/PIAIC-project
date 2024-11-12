class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity


class InventoryManagementSystem:
    def __init__(self):
        self.products = {}
        self.users = {
            'admin': User('admin', 'admin123', 'Admin'),
            'user': User('user', 'user123', 'User')
        }
        self.current_user = None
        self.low_stock_threshold = 10  # Threshold for low stock warning

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            self.current_user = user
            print(f"Login successful! Welcome, {self.current_user.role} {self.current_user.username}.")
            return True
        else:
            print("Invalid username or password. Please try again.")
            return False

    def add_product(self, product_id, name, category, price, stock_quantity):
        if self.current_user.role != 'Admin':
            print("Permission denied: Only Admins can add products.")
            return

        if product_id in self.products:
            print("Product ID already exists. Use a unique ID.")
            return

        new_product = Product(product_id, name, category, price, stock_quantity)
        self.products[product_id] = new_product
        print(f"Product '{name}' added successfully.")

    def edit_product(self, product_id, name=None, category=None, price=None, stock_quantity=None):
        if self.current_user.role != 'Admin':
            print("Permission denied: Only Admins can edit products.")
            return

        product = self.products.get(product_id)
        if not product:
            print("Product not found.")
            return

        if name: product.name = name
        if category: product.category = category
        if price is not None: product.price = price
        if stock_quantity is not None: product.stock_quantity = stock_quantity

        print(f"Product '{product_id}' updated successfully.")

    def delete_product(self, product_id):
        if self.current_user.role != 'Admin':
            print("Permission denied: Only Admins can delete products.")
            return

        if product_id in self.products:
            del self.products[product_id]
            print(f"Product '{product_id}' deleted successfully.")
        else:
            print("Product not found.")

    def view_inventory(self):
        if not self.products:
            print("No products in inventory.")
            return

        print("\nInventory:")
        for product in self.products.values():
            status = "(Low Stock)" if product.stock_quantity <= self.low_stock_threshold else ""
            print(f"ID: {product.product_id}, Name: {product.name}, Category: {product.category}, "
                  f"Price: ${product.price}, Stock: {product.stock_quantity} {status}")
    
    def search_product(self, search_term, search_by="name"):
        found = False
        for product in self.products.values():
            if (search_by == "name" and search_term.lower() in product.name.lower()) or \
               (search_by == "category" and search_term.lower() in product.category.lower()):
                print(f"Found - ID: {product.product_id}, Name: {product.name}, Category: {product.category}, "
                      f"Price: ${product.price}, Stock: {product.stock_quantity}")
                found = True
        if not found:
            print("No matching products found.")

    def adjust_stock(self, product_id, quantity):
        if self.current_user.role != 'Admin':
            print("Permission denied: Only Admins can adjust stock.")
            return

        product = self.products.get(product_id)
        if not product:
            print("Product not found.")
            return

        product.stock_quantity += quantity
        print(f"Stock for product '{product.name}' adjusted by {quantity}. New stock: {product.stock_quantity}")
        if product.stock_quantity <= self.low_stock_threshold:
            print(f"Warning: Low stock for product '{product.name}'! Consider restocking.")

    def main_menu(self):
        print("\nMain Menu:")
        print("1. View Inventory")
        print("2. Search Product by Name")
        print("3. Search Product by Category")
        if self.current_user.role == 'Admin':
            print("4. Add Product")
            print("5. Edit Product")
            print("6. Delete Product")
            print("7. Adjust Stock")

        print("0. Logout")
        
    def run(self):
        print("Welcome to the Inventory Management System!")
        
        # Login prompt
        while True:
            username = input("Username: ")
            password = input("Password: ")
            if self.login(username, password):
                break
        
        # Main system loop
        while True:
            self.main_menu()
            choice = input("Enter choice: ")

            try:
                if choice == "1":
                    self.view_inventory()
                elif choice == "2":
                    search_term = input("Enter product name to search: ")
                    self.search_product(search_term, search_by="name")
                elif choice == "3":
                    search_term = input("Enter product category to search: ")
                    self.search_product(search_term, search_by="category")
                elif choice == "4" and self.current_user.role == 'Admin':
                    product_id = input("Product ID: ")
                    name = input("Product Name: ")
                    category = input("Category: ")
                    price = float(input("Price: "))
                    stock_quantity = int(input("Stock Quantity: "))
                    self.add_product(product_id, name, category, price, stock_quantity)
                elif choice == "5" and self.current_user.role == 'Admin':
                    product_id = input("Product ID to edit: ")
                    name = input("New Product Name (leave blank to keep unchanged): ") or None
                    category = input("New Category (leave blank to keep unchanged): ") or None
                    price = input("New Price (leave blank to keep unchanged): ")
                    price = float(price) if price else None
                    stock_quantity = input("New Stock Quantity (leave blank to keep unchanged): ")
                    stock_quantity = int(stock_quantity) if stock_quantity else None
                    self.edit_product(product_id, name, category, price, stock_quantity)
                elif choice == "6" and self.current_user.role == 'Admin':
                    product_id = input("Product ID to delete: ")
                    self.delete_product(product_id)
                elif choice == "7" and self.current_user.role == 'Admin':
                    product_id = input("Product ID to adjust stock: ")
                    quantity = int(input("Enter quantity to add (positive) or reduce (negative): "))
                    self.adjust_stock(product_id, quantity)
                elif choice == "0":
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice or insufficient permissions. Please try again.")
            except ValueError:
                print("Invalid input. Please enter valid data.")

# Running the system
if __name__ == "__main__":
    ims = InventoryManagementSystem()
    ims.run()
