from models.sale_item import SaleItem


class Sale:

    def __init__(
        self,
        customer_id,
        subtotal,
        discount=0,
        gst=0,
        payment_method="Cash"
    ):
        self.customer_id = customer_id
        self.subtotal = subtotal
        self.discount = discount
        self.gst = gst
        self.payment_method = payment_method

        self.total = (
            subtotal
            - discount
            + gst
        )

        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def display_sale(self):

        print(f"Customer ID: {self.customer_id}")
        print(f"Subtotal: ₹{self.subtotal}")
        print(f"Discount: ₹{self.discount}")
        print(f"GST: ₹{self.gst}")
        print(f"Payment: {self.payment_method}")
        print(f"Total: ₹{self.total}")

        print("\nItems:")

        for item in self.items:
            print(
                item.product_id,
                item.quantity,
                item.price,
                item.total
            )


if __name__ == "__main__":

    sale = Sale(
        customer_id=1,
        subtotal=1800,
        discount=100,
        gst=306
    )

    item1 = SaleItem(
        product_id=1,
        quantity=2,
        price=500
    )

    item2 = SaleItem(
        product_id=2,
        quantity=1,
        price=800
    )

    sale.add_item(item1)
    sale.add_item(item2)

    sale.display_sale()