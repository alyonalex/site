from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from sqlalchemy.orm import relationship

Base = declarative_base()  
  
# здесь добавим классы 
class Rooms(Base):
    __tablename__ = 'rooms'
    room_id = Column(Integer, primary_key=True)
    room_name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    cost = Column(Float, nullable=False) 
    order = relationship("Orders", backref='rooms')

class Equipment(Base):
    __tablename__ = 'equipment'
    equipment_id = Column(Integer, primary_key=True)
    equipment_name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    cost = Column(Float, nullable=False)
    order = relationship("Orders", backref='equipment')

class Clients(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True)
    client_name = Column(String(50), nullable=False)
    client_surname = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    order = relationship("Orders", backref='clients')

class Orders(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.client_id'))
    room_id = Column(Integer, ForeignKey('rooms.room_id'))
    day = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    duration = Column(Integer, nullable=False)
    equipment_id = Column(Integer, ForeignKey('equipment.equipment_id'))


engine = create_engine('sqlite:///studio.db')  
Base.metadata.create_all(engine)


