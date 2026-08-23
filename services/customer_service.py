from database.db_connection import get_connection
from models.customer import Customer


class CustomerService:

    # CREATE
    def add_customer(self, customer):

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO customers
                (name, phone, email, address)
                VALUES (?, ?, ?, ?)
            """, (
                customer.name,
                customer.phone,
                customer.email,
                customer.address
            ))

            connection.commit()

            print("Customer added successfully!")

        except Exception as e:
            print("Database error:", e)

        finally:
            if connection:
                connection.close()

    # READ
    def get_all_customers(self):

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM customers")

            customers = cursor.fetchall()

            return customers

        except Exception as e:
            print("Database error:", e)
            return []

        finally:
            if connection:
                connection.close()

    # UPDATE
    def update_customer(self, customer_id, phone, email, address):

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE customers
                SET phone = ?, email = ?, address = ?
                WHERE customer_id = ?
            """, (
                phone,
                email,
                address,
                customer_id
            ))

            connection.commit()

            if cursor.rowcount == 0:
                print("Customer not found.")
            else:
                print("Customer updated successfully!")

        except Exception as e:
            print("Database error:", e)

        finally:
            if connection:
                connection.close()

    # DELETE
    def delete_customer(self, customer_id):

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM customers
                WHERE customer_id = ?
            """, (customer_id,))

            connection.commit()

            if cursor.rowcount == 0:
                print("Customer not found.")
            else:
                print("Customer deleted successfully!")

        except Exception as e:
            print("Database error:", e)

        finally:
            if connection:
                connection.close()


# Testing
if __name__ == "__main__":

    service = CustomerService()

    customer = Customer(
        "Parth",
        "9876543210",
        "parth@example.com",
        "Pune"
    )

    # CREATE
    service.add_customer(customer)

    # READ
    customers = service.get_all_customers()

    print("\nAll Customers:")

    for customer in customers:
        print(customer)

    # UPDATE
    # service.update_customer(
    #     1,
    #     "9876543211",
    #     "new@example.com",
    #     "Mumbai"
    # )

    # DELETE
    # service.delete_customer(1)