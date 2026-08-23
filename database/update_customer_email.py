from database.db_connection import get_connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    UPDATE customers
    SET email = ?
    WHERE customer_id = ?
""", (
    "parthbhor0225@gmail.com",
    1
))

connection.commit()
connection.close()

print("Customer email updated successfully!")