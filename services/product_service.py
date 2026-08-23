from database.db_connection import get_connection
from models.product import Product
from utils.validators import validate_product

class ProductService:

    # CREATE
    def add_product(self, product):

        validate_product(
            product.name,
            product.category,
            product.price,
            product.quantity
        )

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO products
                (name, category, price, quantity, supplier_id)
                VALUES (?, ?, ?, ?, ?)
            """, (
                product.name,
                product.category,
                product.price,
                product.quantity,
                product.supplier_id
            ))

            connection.commit()

            print("Product added successfully!")

        except Exception as e:
            print("Database error:", e)

        finally:
            if connection:
                connection.close()

    # READ
    def get_all_products(self):

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM products")

            products = cursor.fetchall()

            return products

        except Exception as e:
            print("Database error:", e)
            return []

        finally:
            if connection:
                connection.close()

    # UPDATE
    def update_product(self, product_id, price, quantity):

        if price < 0:
            raise ValueError("Price cannot be negative.")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE products
                SET price = ?, quantity = ?
                WHERE product_id = ?
            """, (
                price,
                quantity,
                product_id
            ))

            connection.commit()

            if cursor.rowcount == 0:
                print("Product not found.")
            else:
                print("Product updated successfully!")

        except Exception as e:
            print("Database error:", e)

        finally:
            if connection:
                connection.close()

    # DELETE
    def delete_product(self, product_id):

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM products
                WHERE product_id = ?
            """, (product_id,))

            connection.commit()

            if cursor.rowcount == 0:
                print("Product not found.")
            else:
                print("Product deleted successfully!")

        except Exception as e:
            print("Database error:", e)

        finally:
            if connection:
                connection.close()


# Testing
if __name__ == "__main__":

    service = ProductService()

    # CREATE
    product = Product(
        "Wireless Mouse",
        "Electronics",
        500,
        20
    )

    service.add_product(product)

    # READ
    products = service.get_all_products()

    print("\nAll Products:")

    for product in products:
        print(product)

    # UPDATE
    service.update_product(1, 550, 25)

    # DELETE
    # service.delete_product(1)