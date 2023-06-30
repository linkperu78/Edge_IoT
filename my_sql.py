# Librerias para SQL
import sqlalchemy as SQL
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
import datetime

name_db = "dato.db"

def create_engine(name_database = name_db):
    return SQL.create_engine(f"sqlite:///instance/{name_database}")

def create_session(engine):
    Session = sessionmaker( bind = engine )
    return Session()


def create_db(database_name):
    engine = create_engine(database_name)
    if database_exists(engine.url):
        return f"Database {database_name} : Already exists" 
    create_database(engine.url)
    return f"Database {database_name} : Created"


def check_db(database_name):
    print(f"\n\t ** Evaluando la base de datos: / {database_name} / **")
    engine = create_engine(database_name)
    session = create_session(engine)
    metadata = SQL.MetaData()
    metadata.reflect(bind = engine)

    for table_name, table in metadata.tables.items():
        print("")
        #print(f"{table_name} - {table.columns.keys()}")
        row_count = 0
        with engine.connect() as connection:
            query = SQL.text(f"SELECT COUNT(*) FROM {table_name}")
            result = connection.execute(query)
            row_count = result.scalar()
            #print(row_count)
        print(f"\t Table name = ** {table_name} **  with {row_count} datos")
        for column in table.c:
            print(f' - Column: {column.name} | Type: {column.type}')

def get_tables_names(new_name_db = name_db):
    engine = create_engine(new_name_db)
    metadata = SQL.MetaData()
    metadata.reflect(bind = engine)
    array_table = []
    for table_name, table in metadata.tables.items():
        array_table.append(table_name)
    return array_table
        

def create_table(name_db, Model):
    engine = create_engine(name_db)
    session = create_session(engine)
    Model.metadata.create_all(bind = engine)
    session.close()
    return(f"Table '{Model.__tablename__}' created successfully.")


def insert_data(Model, array_data):
    try:
        engine = create_engine(name_db)
        session = create_session(engine)
        new_data = Model(P = array_data['P'], I = array_data['I'], F = array_data['F'])
        session.add(new_data)
        session.commit()
        print("Sucess")
    except Exception as e:
        print(f"{e}")


def get_values(database, Model_table, offset, qty):
    engine = create_engine(database)
    session = create_session(engine)
    results = ( session.query(Model_table)
               .order_by(Model_table.Id)
               .offset(offset)
               .limit(qty)
               .all() )
    for r in results:
        new_fecha = r.Fecha
        dt_format = datetime.datetime.fromtimestamp(new_fecha)
        date_string = dt_format.strftime('%Y-%m-%d')
        msg = f"Id = {r.Id} - P = {r.P}\t - F = {r.F}\t - Fecha = {date_string}\t - I = {r.I}"
        print(msg)


def get_all_values(database, Model_table):
    engine = create_engine(database)
    session = create_session(engine)
    results = ( session.query(Model_table)
               .order_by(Model_table.Id)
               #.offset(offset)
               #.limit(qty)
               .all() )
    for r in results:
        msg = f"Id = {r.Id} - P = {r.P} - F = {r.F} - I = {r.I}"
        print(msg)

def export_data(database, Model_source, Model_destiny):
    try:
        engine = create_engine(database)
        session = create_session(engine)
        #Get all data from source
        original_data = session.query(Model_source).all()

        for row in original_data:
            new_fecha_int = int(row.F)
            destination_row = Model_destiny(
                Id = row.Id,
                P = row.P,
                F = row.F,
                I = row.I,
                Fecha = new_fecha_int
            )
            session.add(destination_row)
        session.commit()

    except Exception as e:
        print(f"Error : {e}")


def copy_table(name_db, name_original, name_copy):
    engine = create_engine(name_db)
    session = create_session(engine)
    metadata = SQL.MetaData()

    source_table = SQL.Table(name_original, metadata, autoload=True, autoload_with=engine)

    target_table = source_table.tometadata(metadata, name = name_copy)
    target_table.create(bind=engine, checkfirst=True)
    session.execute(target_table.insert().from_select(target_table.columns.keys(), source_table.select()))
    session.commit()

'''
    def get_data_from(self, name_id):
        model = self.model
        session = self.connect_to_db()
        results = session.query(model).filter_by(I = name_id).all()
        values = [result.P for result in results]
        return values
    

    def get_data_timestamp(self, name_id):
        model = self.model
        session = self.connect_to_db()
        results = session.query(model).filter_by(I = name_id).all()
        values = [result.F for result in results]
        return values
'''