from sqlalchemy import create_engine, MetaData, Table

# Step 1: Establish a connection to the database
engine = create_engine('sqlite:///instance/dato.db')

# Step 2: Create a metadata object
metadata = MetaData()

# Step 3: Load the metadata of the existing tables
metadata.reflect(bind = engine)

# Step 4: Get the table name you want to delete
table_name = 'salud_table'

# Step 5: Check if the table exists in the database
if table_name in metadata.tables:
    # Step 7: Get the table object
    table = Table(table_name, metadata, autoload=True, autoload_with=engine)

    # Step 8: Drop the table
    table.drop(bind=engine)
    print(f"Table '{table_name}' deleted successfully.")
else:
    print(f"Table '{table_name}' does not exist in the database.")
