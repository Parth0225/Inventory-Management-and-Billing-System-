from database.db_connection import get_connection
from models.supplier import Supplier


class SupplierService:

    # CREATE
    def add_supplier(self, supplier):

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO suppliers
                (name, company, phone, email, address)
                VALUES (?, ?, ?, ?, ?)
            """, (
                supplier.name,
                supplier.company,
                supplier.phone,
                supplier.email,
                supplier.address
            ))

            connection.commit()

            print("Supplier added successfully!")

        except Exception as e:
            print("Database error:", e)

        finally:
            if connection:
                connection.close()

    # READ
    def get_all_suppliers(self):

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM suppliers")

            suppliers = cursor.fetchall()

            return suppliers

        except Exception as e:
            print("Database error:", e)
            return []

        finally:
            if connection:
                connection.close()

    # UPDATE
    def update_supplier(
        self,
        supplier_id,
        phone,
        email,
        address
    ):

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE suppliers
                SET phone = ?, email = ?, address = ?
                WHERE supplier_id = ?
            """, (
                phone,
                email,
                address,
                supplier_id
            ))

            connection.commit()

            if cursor.rowcount == 0:
                print("Supplier not found.")
            else:
                print("Supplier updated successfully!")

        except Exception as e:
            print("Database error:", e)

        finally:
            if connection:
                connection.close()

    # DELETE
    def delete_supplier(self, supplier_id):

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM suppliers
                WHERE supplier_id = ?
            """, (supplier_id,))

            connection.commit()

            if cursor.rowcount == 0:
                print("Supplier not found.")
            else:
                print("Supplier deleted successfully!")

        except Exception as e:
            print("Database error:", e)

        finally:
            if connection:
                connection.close()


# Testing
if __name__ == "__main__":

    service = SupplierService()

    supplier = Supplier(
        "Rahul Sharma",
        "ABC Electronics",
        "9876543210",
        "abc@example.com",
        "Pune"
    )

    # CREATE
    service.add_supplier(supplier)

    # READ
    suppliers = service.get_all_suppliers()

    print("\nAll Suppliers:")

    for supplier in suppliers:
        print(supplier)

    # UPDATE
    # service.update_supplier(
    #     1,
    #     "9876543211",
    #     "new@example.com",
    #     "Mumbai"
    # )

    # DELETE
    # service.delete_supplier(1)