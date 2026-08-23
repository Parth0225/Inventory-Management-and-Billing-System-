class Product:

    def __init__(self, name, category, price, quantity, supplier_id=None):
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.supplier_id = supplier_id

    def display_product(self):
        print(f"Product: {self.name}")
        print(f"Category: {self.category}")
        print(f"Price: ₹{self.price}")
        print(f"Quantity: {self.quantity}")

if __name__ == "__main__":

    product = Product(
        "Wireless Mouse",
        "Electronics",
        500,
        20
    )

    product.display_product()