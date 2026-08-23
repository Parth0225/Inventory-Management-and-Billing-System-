class Supplier:

    def __init__(self, name, company, phone, email, address):
        self.name = name
        self.company = company
        self.phone = phone
        self.email = email
        self.address = address

    def display_supplier(self):
        print(f"Supplier: {self.name}")
        print(f"Company: {self.company}")
        print(f"Phone: {self.phone}")
        print(f"Email: {self.email}")
        print(f"Address: {self.address}")