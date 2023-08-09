# Librerias para SQL
import sqlalchemy   as SQL
from sqlalchemy_utils   import database_exists, create_database
from sqlalchemy.orm     import sessionmaker
import models as M
import datetime

class sql_host():
    def __init__(self):
        pass
    
    def set_name_db(self, name_db):
        self.db_name = name_db + ".db"
        self.engine = SQL.create_engine(f"sqlite:///instance/{self.db_name}")
        Session = sessionmaker(bind = self.engine)
        self.session = Session()

    def create_db(self):
        if database_exists(self.engine.url):
            print(f"Database {self.db_name} : Already exists")
            return 
        create_database(self.engine.url)
        print(f"Database {self.db_name} : Created")


    def check_db(self):
        print(f"\n\t ** Evaluando la base de datos: / {self.db_name} / **")
        metadata = SQL.MetaData()
        metadata.reflect( bind = self.engine )
        for table_name, table in metadata.tables.items():
            row_count = 0
            with self.engine.connect() as connection:
                query = SQL.text(f"SELECT COUNT(*) FROM {table_name}")
                result = connection.execute(query)
                row_count = result.scalar()
                #print(row_count)
            print(f"\t Table name = ** {table_name} **  with {row_count} datos")
            for column in table.c:
                print(f' - Column: {column.name} | Type: {column.type}')


    def get_tables_names(self):
        metadata = SQL.MetaData()
        metadata.reflect(bind = self.engine)
        array_table = []
        for table_name, table in metadata.tables.items():
            array_table.append(table_name)
            #print(f" - Tabla encontrada = {table_name}")
        return array_table
            

    def create_table(self, Model):
        Model.metadata.create_all(bind = self.engine)
        return(f"Table '{Model.__tablename__}' created successfully.")


    # Ingresamos un nuevo dato a la tabla usando el MODEL de la tabla
    def insert_data(self, Model, data_dictionary):
        try:
            p_value = data_dictionary['P']
            i_value = data_dictionary['I']
            f_value = data_dictionary['F']
            fecha = data_dictionary["Fecha"]
            new_data = Model(P = p_value, 
                             I = i_value, 
                             F = f_value,
                             Fecha = fecha)
            self.session.add(new_data)
            self.session.commit()
            print(f"{Model.__tablename__} : P = {p_value}, F = {f_value}, I = {i_value}")
        except Exception as e:
            print(f"{e}")


    # Copy the table to another one
    def copy_table(self, name_original, name_copy):
        metadata = SQL.MetaData()
        source_table = SQL.Table(name_original, metadata, autoload=True, autoload_with = self.engine)
        target_table = source_table.tometadata(metadata, name = name_copy)
        target_table.create(bind = self.engine, checkfirst=True)
        self.session.execute(target_table.insert().from_select(target_table.columns.keys(), source_table.select()))
        self.session.commit()

    
    # Obtenemos MODEL de la tabla SQL del dia actual
    def get_today_table(self):
        current_date = datetime.datetime.now().strftime('%Y_%m_%d')
        #print("Buscando las bases de datos")
        tables_names = self.get_tables_names()
        found = 0
        my_table_actual_name = "Salud_TPI_" + current_date
        for name_table in tables_names:
            # Si encontro una base de datos de hoy, no crea una nueva base 
            if (name_table == my_table_actual_name) :
                found = 1
                break

        # Encontramos una base de datos de hoy, seguimos usandolo
        new_model = M.create_model_salud(my_table_actual_name)
        if found == 0:
            # Como no encontramos una base de datos de hoy, creamos una nueva base
            # y transferimos todos los datos en la tabla de no enviados a esta tabla
            self.create_table(new_model)
        return new_model
    

    # Finalizamos el host
    def end_host(self):
        self.session.close()
