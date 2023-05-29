import sqlite3

# Connect to the database
connection = sqlite3.connect('instance/dato.db')
cursor = connection.cursor()

# Query the last 10 rows in the table by ID
query = "SELECT * FROM salud_table ORDER BY ID DESC LIMIT 10"
cursor.execute(query)
results = cursor.fetchall()

# Print the retrieved rows
for row in results:
    print(row)

# Close the database connection
connection.close()