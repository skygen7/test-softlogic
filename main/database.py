from sqlalchemy import Integer, Column, ARRAY, Text, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from main.settings import load_config
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    surname = Column(Text)
    vector = Column(ARRAY(Float))

    def __init__(self, name, surname, vector):
        self.name = name
        self.surname = surname
        self.vector = vector

    def __repr__(self):
        return f"<Person({self.name}, {self.surname}, {self.vector})>"


engine = create_engine(load_config().get('db_parameters'))

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
