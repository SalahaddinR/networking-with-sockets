from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('mysql+pymysql://root:k2797181@localhost:3306/order_service')
Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer(), primary_key=True)
    client_name = Column(String(128))
    client_email = Column(String(128), unique=True)
    client_password = Column(String(128))

    def __init__(self, name: str, email: str, password: str):
        self.client_name = name
        self.client_email = email
        self.set_password(password)
        
    def set_password(self, password: str):
        self.client_password = generate_password_hash(password=password)
        
    def check_password(self, password: str):
        return check_password_hash(self.client_password, password)
        
    def __repr__(self):
        return "Client(name={}, email={})".format(self.client_name, self.client_email)

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer(), primary_key=True)
    client_id = Column(Integer(), ForeignKey('clients.client_id'))
    order_name = Column(String(128))
    order_amount = Column(Integer())
    order_time = Column(DateTime(), default=datetime.today)

    order = relationship('Client', backref=backref('orders'))

    def __init__(self, name: str, amount: int, client_id: int):
        self.order_name = name
        self.order_amount = amount
        self.client_id = client_id

    def __repr__(self):
        return "Order(name={}, amount={}, client={})".format(self.order_name, self.order_amount, self.client_id)

Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()

