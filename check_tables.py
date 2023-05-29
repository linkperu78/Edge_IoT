from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# Create a SQLAlchemy engine
engine = create_engine('sqlite:///instance/dato.db')

# Create an inspector object
inspector = inspect(engine)

# Get the table names in the database
table_names = inspector.get_table_names()

# Iterate over the table names and get the column names for each table
for table_name in table_names:
    print(table_name)
    columns = inspector.get_columns(table_name)
    for column in columns:
        column_name = column['name']
        column_type = column['type']
        column_key = column['primary_key']
        print(f"Column name = {column_name} - {column_type} - PK = {column_key}")
    