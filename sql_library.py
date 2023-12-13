# Librerias para SQL
import sqlalchemy   as SQL
from sqlalchemy_utils   import database_exists, create_database
from sqlalchemy.orm     import sessionmaker

# Models is for abreviating SQL request when it is needed to
# make as input the format of the table or data
import models as M

# With this class, we will have a preparated
# SQL hoster to make request using its functions
class sql_host():
    # When the sql_host is created
    def __init__(self):
        pass
    
    # Set the direction of the database sql which we will use
    # i.e. my_sql_database.db will set with: [sql_host.set_name_db("my_sql_database")]
    def set_name_db(self, name_db):
        self.db_name = name_db + ".db"
        self.engine = SQL.create_engine(f"sqlite:///instance/{self.db_name}")
        Session = sessionmaker(bind = self.engine)
        self.session = Session()
        print(f"Nombre de la base de dato = {name_db}\n")

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

    # Ingresamos un nuevo dato a la tabla usando el MODEL
    def insert_data(self, Model, data_dictionary):
        try:
            print(f"Data a ingresar = {data_dictionary}\n")
            self.session.add(Model(**data_dictionary))
            self.session.commit()
            #print(f"{Model.__tablename__} : {data_dictionary}")
        except Exception as e:
            print(f"Error en insertar datos =\n{e}\n")

    # Copy the table to another one
    def copy_table(self, name_original, name_copy):
        metadata = SQL.MetaData()
        source_table = SQL.Table(name_original, metadata, autoload=True, autoload_with = self.engine)
        target_table = source_table.tometadata(metadata, name = name_copy)
        target_table.create(bind = self.engine, checkfirst=True)
        self.session.execute(target_table.insert().from_select(target_table.columns.keys(), source_table.select()))
        self.session.commit()
    
    # Eliminamos la tabla de datos deseada
    def delete_table(self, Model):
        metadata = SQL.MetaData()
        metadata.reflect(bind = self.engine)
        Model.__table__.drop(self.engine)

    def delete_all_tables(self):
        metadata = SQL.MetaData()
        metadata.reflect(bind = self.engine)
        inspector = SQL.inspect(self.engine)
        table_names = inspector.get_table_names()

        for table_name in table_names:
            table = metadata.tables.get(table_name)
            if table is not None:
                table.drop(self.engine)

    # Finalizamos el host
    def end_host(self):
        self.engine.dispose()
        self.session.close()
