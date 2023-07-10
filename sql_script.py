import my_sql
import models as M
import header_values as const
# By default:
# Database      = dato.db
# Table_name    = salud_table

print(" ----------- Comenzando la declaracion de variables -----------")

database_name_default = "dato.db"

#actual_model = M.create_model("salud_table")
new_model = M.Salud_NE()

print(" ----------- Comenzando la solucion ----------- ")
#my_test_model = M.Salud

# Create database
#print(my_sql.create_db("dato.db"))

# Insert data
#my_sql.insert_data(my_test_model, data_test)

# Create a new table
#my_sql.create_table(database_name_default, new_model)

# Export Data
#my_sql.export_data(database_name_default, actual_model, new_model)

# View example of data in table
#my_sql.get_all_values(database_name_default, my_test_model)

# Check some values
#my_sql.get_values(database_name_default, new_model, 900, 300)

# Check Database
my_sql.check_db(database_name_default)
