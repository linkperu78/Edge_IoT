import sqlalchemy as db
import models as model
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

# Funciones para manejar creacion, chequeo o eliminacion

#Creacion de clases
class table_stats:
    def __init__(self, database = "dato.db", table_name = "salud_table"):
        self.database = database
        self.table_name = table_name
        self.engine = db.create_engine(f"sqlite:///instance/{database}")
        #self.enginenn = db.create_engine(f"sqlite:///{database}", echo = True)
    def get_database(self):
        return self.database
    
    def get_table_name(self):
        return self.table_name

    # Creacion de base de datos
    def create_db(self):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)


    # Eliminacion de la base de datos
    def delete_db(self):
        return "Eliminalo manualmente mano"

    # Creacion de la tabla
    def create_table(self):
        metadata = db.MetaData()
        columns = [
            db.Column("Id", db.Integer, primary_key=True),
            db.Column('P', db.Float),
            db.Column('F', db.String(30)),
            db.Column('I', db.String(30))
        ]
        table = db.Table(self.table_name, metadata, *columns)
        table.create(bind=self.engine)
        print(f"Table '{self.table_name}' created successfully.")


    # Chequeo de la tabla
    def check_table(self):
        with self.engine.connect() as conn:
            inspector  = db.inspect(conn)
            columns = inspector.get_columns(self.table_name)
        for column in columns:
            print(f"Column name: {column['name']}")
            print(f"Type: {column['type']}")

    
    # Clear the tabla data
    def clear_table(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        # Define the table and metadata
        metadata = db.MetaData()
        metadata.reflect(bind=self.engine)
        your_table = metadata.tables[self.table_name]

        # Clear data in the table
        delete_statement = your_table.delete()
        session.execute(delete_statement)
        session.commit()

        # Close the session
        session.close()


