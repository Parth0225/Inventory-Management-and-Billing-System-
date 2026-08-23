from database.db_connection import get_connection
from models.sale import Sale


class BillingService:

    def create_sale(self, sale):

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            # 1. Check customer
            cursor.execute("""
                SELECT customer_id
                FROM customers
                WHERE customer_id = ?
            """, (sale.customer_id,))

            customer = cursor.fetchone()

            if customer is None:
                raise ValueError("Customer not found.")

            # 2. Check all products and stock
            for item in sale.items:

                cursor.execute("""
                    SELECT quantity, price
                    FROM products
                    WHERE product_id = ?
                """, (item.product_id,))

                product = cursor.fetchone()

                if product is None:
                    raise ValueError(
                        print(f"Product ID {item.product_id} not found.")
                    )

                current_stock = product[0]

                if item.quantity <= 0:
                    raise ValueError(
                        print("Quantity must be greater than 0.")
                    )

                if item.quantity > current_stock:
                    raise ValueError(
                        print(f"Not enough stock for product ID "
                              f"{item.product_id}.")
                    )

            # 3. Insert sale
            cursor.execute("""
                INSERT INTO sales
                (
                    customer_id,
                    sale_date,
                    subtotal,
                    discount,
                    gst,
                    total,
                    payment_method
                )
                VALUES (?, datetime('now'), ?, ?, ?, ?, ?)
            """, (
                sale.customer_id,
                sale.subtotal,
                sale.discount,
                sale.gst,
                sale.total,
                sale.payment_method
            ))

            sale_id = cursor.lastrowid

            # 4. Insert sale items + reduce stock
            for item in sale.items:

                cursor.execute("""
                    INSERT INTO sale_items
                    (sale_id, product_id, quantity, price, total)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    sale_id,
                    item.product_id,
                    item.quantity,
                    item.price,
                    item.total
                ))

                cursor.execute("""
                    UPDATE products
                    SET quantity = quantity - ?
                    WHERE product_id = ?
                """, (
                    item.quantity,
                    item.product_id
                ))

            # 5. Save everything
            connection.commit()

            print("Sale created successfully!")
            print(f"Sale ID: {sale_id}")

            return sale_id

        except Exception as e:

            if connection:
                connection.rollback()

            print("Billing error:", e)

            return None

        finally:

            if connection:
                connection.close()


# Testing
if __name__ == "__main__":

    service = BillingService()

    sale = Sale(
        customer_id=1,
        subtotal=1800,
        discount=100,
        gst=306
    )

    from models.sale_item import SaleItem

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

    service.create_sale(sale)