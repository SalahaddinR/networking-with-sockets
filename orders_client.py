import socket

DISCONNECT_MSG = 'command:disconnect'
SUCCESS_MSG_01 = 'info:verified'
SUCCESS_MSG_02 = 'info:registered'
FAILURE_MSG_01 = 'info:verification-failed'
CODING_FORMAT = 'UTF-8'

def create_tcp_client(host: str, port: int, ip_version = socket.AF_INET) -> socket.socket:
    tcp_client = socket.socket(ip_version, socket.SOCK_STREAM)  
    tcp_client.connect((host, port))
    return tcp_client

def user_verification(tcp_client: socket.socket, buffer_size: int = 1024):
    print('\nLOG IN')
    email = input('>email: ')
    password = input('>password: ')
    message = "type:client:verify:email={}|pword={}|".format(email, password)

    tcp_client.send(message.encode(CODING_FORMAT))
    back_msg  = tcp_client.recv(buffer_size).decode(CODING_FORMAT)
    if back_msg == SUCCESS_MSG_01:
        print('...credentials verified!')
        client_id = int(tcp_client.recv(buffer_size).decode(CODING_FORMAT))
        return client_id
    elif back_msg == FAILURE_MSG_01:
        print('...invalid credentials!')
        command = input('> do you wanna to sing in? ')
        if command.lower() in ['y', 'yes']:
            result = user_registration(tcp_client)
            return result

def user_registration(tcp_client: socket.socket, buffer_size: int = 1024):
    print('\nSING IN')
    name = input('>name: ')
    email = input('>email: ')
    password = input('>password: ')
    message = "type:client:register:name={}|email={}|pword={}|".format(name, email, password)

    tcp_client.send(message.encode(CODING_FORMAT))
    back_msg = tcp_client.recv(buffer_size).decode(CODING_FORMAT)
    if back_msg == SUCCESS_MSG_02:
        print('...registration data accepted')
        print('...remember your password!< {} >'.format(password))
        client_id = int(tcp_client.recv(buffer_size).decode(CODING_FORMAT))
        return client_id
    #tcp_client.send(DISCONNECT_MSG.encode(CODING_FORMAT))


def order_registration(tcp_client: socket.socket, client_id: int, buffer_size: int = 1024):
    if not client_id: return
    print('\nORDER REGISTRATION')
    name = input('>order name: ')
    amount = input('>order amount: ')
    message = "type:order:register:name={}|amount={}|id={}|".format(name, amount, client_id)

    tcp_client.send(message.encode(CODING_FORMAT))
    back_msg = tcp_client.recv(buffer_size).decode(CODING_FORMAT)
    if back_msg == SUCCESS_MSG_02:
        print('...your order accepted!')
    tcp_client.send(DISCONNECT_MSG.encode(CODING_FORMAT))


def take_order():
    tcp_client = create_tcp_client('192.168.143.17', 5000)

    client_id = user_verification(tcp_client)
    order_registration(tcp_client, client_id)

take_order()





