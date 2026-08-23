from database.db_connection import get_connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT customer_id, name, email
    FROM customers
""")

customers = cursor.fetchall()

for customer in customers:
    print(customer)

connection.close()