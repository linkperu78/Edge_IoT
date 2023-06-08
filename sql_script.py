import my_sql as f

# By default:
# Database      = dato.db
# Table_name    = salud_table
my_table = f.table_stats()

# Create database
#print(my_table.create_db())

# Delete database
#print(my_table.delete_db())

# Create table
#print(my_table.create_table())

# Check table
print(my_table.check_table())

# Clear table
#print(my_table.clear_table())

# Delete table
#print(my_table.delete_table())

