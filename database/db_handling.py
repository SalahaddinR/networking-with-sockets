from sqlalchemy.orm.decl_api import DeclarativeMeta
from .db_schema import session, Client, Order

def prevent_dublicate(model, comp_attr_1: str, comp_attr_2: str):
    '''
    Decorator to prevent dublication data model rows in database
    Returns the instance of data model row if it is not exists
    Otherwise it returns existing data model from database
    '''
    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)

            comparison = session.query(model).filter(
                model.__getattribute__(model, comp_attr_1) == result.__getattribute__(comp_attr_1),
                model.__getattribute__(model, comp_attr_2) == result.__getattribute__(comp_attr_2)
            ).first()

            if comparison is not None:
                return comparison
            else:
                return result
        return wrapper
    return decorator
            
def save_changes(function):
    '''
    Recives function which returns data model row and it saves it in database
    '''
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        session.add(result)
        session.commit()
        return result
    return wrapper

@save_changes
@prevent_dublicate(Client, 'client_name', 'client_email')
def insert_client(name: str, email: str, password: str):
    new_client = Client(name, email, password)
    return new_client

@save_changes
def insert_order(name: str, amount: int, client_data: int):
    client_id = session.query(Client).filter_by(client_id=client_data)
    if client_id is not None:
        client_id = client_id.first().client_id
        new_order = Order(name, amount, client_id)
        return new_order


def verify_client(email: str, password:str):
    searching_result = session.query(Client).filter(
        Client.client_email == email,
    ).first()
    if searching_result is None:
        return None
    if searching_result.check_password(password):
        return searching_result
    else:
        return None

def client_orders(email: str):
    client = session.query(Client).filter_by(client_email=email).first()
    return client.orders

