from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Addition(Base):
    __tablename__ = "additions"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)

    def __init__(self, name):
        self.name = name
        
class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)

    def __init__(self, name):
        self.name = name
        
# class Order(Base):
#     __tablename__ = "orders"

#     ticket = Column(Integer, primary_key=True)
#     address = Column(String(80))
#     client = Column(String(80))

#     def __init__(self, client):
#         self.client = client