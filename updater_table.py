import my_sql as mySQL
import datetime
import time
import models as M

current_date = datetime.datetime.now().strftime('%Y-%m-%d')


def get_time_sql():
    engine = mySQL.create_engine()
    session = mySQL.create_session(engine)
    print("Buscando las bases de datos")
    tables_names = mySQL.get_tables_names()
    found = 0

    my_table_actual_name = "Salud_TPI_" + current_date

    for name_table in tables_names:
        # Si encontro una base de datos de hoy, no crea una nueva base 
        if (name_table == my_table_actual_name) :
            found = 1
            break
    # Encontramos una base de datos de hoy, seguimos usandolo
    if found == 1:
        return 1

    new_model = M.create_model_tpi(my_table_actual_name)


    # Como no encontramos una base de datos de hoy, creamos una nueva base
    # y transferimos todos los datos en la tabla de no enviados a esta tabla
    mySQL.create_table(mySQL.name_db, new_model)

    # Transferimos los datos de los no Enviados a la nueva base de datos

         


get_time_sql()



