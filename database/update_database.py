from database.db_connection import get_connection


connection = get_connection()
cursor = connection.cursor()

# Check existing columns
cursor.execute("PRAGMA table_info(sales)")

columns = cursor.fetchall()

column_names = [
    column[1]
    for column in columns
]

# Add payment_method only if it doesn't exist
if "payment_method" not in column_names:

    cursor.execute("""
        ALTER TABLE sales
        ADD COLUMN payment_method TEXT DEFAULT 'Cash'
    """)

    connection.commit()

    print("payment_method column added successfully!")

else:

    print("payment_method column already exists.")

connection.close()