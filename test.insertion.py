from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Salud as Data

def connect_to_db(db_uri):
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    return Session()

def insert_data(P_value, I_value, F_value, session):
    new_data = Data(P=P_value, I=I_value, F=F_value)
    session.add(new_data)
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print("Error occurred:", e)
        return None
    return new_data

# Database URI
db_uri = 'sqlite:///instance/dato.db'

# Creating a new session
session = connect_to_db(db_uri)

# Inserting new data
new_data = insert_data(1223.456, 'SomeValueI', 'SomeValueF', session)