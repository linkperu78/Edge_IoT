from sqlalchemy import create_engine, Column, Float, String, Integer, MetaData, Table

# Step 1: Establish a connection to the database
engine = create_engine('sqlite:///instance/dato.db')
# Step 2: Create a metadata object
metadata = MetaData()

# Step 3: Get the table name you want to create
table_name = 'salud_table'

# Step 4: Define the columns for the table
columns = [
    Column("Id", Integer, primary_key=True),
    Column('P', Float),
    Column('F', String(50)),
    Column('I', String(50))
]

# Step 5: Create the table object
table = Table(table_name, metadata, *columns)

# Step 6: Create the table in the database
table.create(bind=engine)

print(f"Table '{table_name}' created successfully.")
