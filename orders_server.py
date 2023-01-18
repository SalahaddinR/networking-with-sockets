import socket, threading
from database import insert_client, insert_order, verify_client, client_orders
from command_analysator import dispatch_command

DISCONNECT_MSG = 'command:disconnect'
SUCCESS_MSG_01 = 'info:verified'
SUCCESS_MSG_02 = 'info:registered'
FAILURE_MSG_01 = 'info:verification-failed'

def create_tcp_server(host: str, port: int, ip_version= socket.AF_INET) -> socket.socket:
    tcp_server = socket.socket(family=ip_version, type=socket.SOCK_STREAM)
    try:
        tcp_server.bind((host, port))
    except socket.error as error:
        print('[SERVER][ERROR] msg: {}'.format(error))
    else:
        return tcp_server

def establish_tcp_connection(tcp_server: socket.socket, clients_amount: int = 5):
    print('[SERVER][SUCCESS] server successfully launched running on {}'.format(tcp_server.getsockname()))
    while True:
        try:
            tcp_server.listen(clients_amount)
            try:
                client, addr = tcp_server.accept()
            except socket.error as error:
                print('[SERVER][ERROR] msg: {}'.format(error))
        except socket.error as error:
            print('[SERVER][ERROR] msg: {}'.format(error))
        else:   
            thread = threading.Thread(target=handle_tcp_client, args=(client, addr))
            thread.start()

def handle_tcp_client(tcp_client: socket.socket, address, fmt: str = "utf-8", buffer_size: int = 1024):
    connected = True
    while connected:
        main_data = tcp_client.recv(buffer_size).decode(fmt)
        if main_data == DISCONNECT_MSG:
            connected = False; continue
        result = dispatch_command(main_data)

        if result.__class__.__name__ == 'RegistrationData':
            client = insert_client(result.name, result.email, result.password)
            print("[SERVER][SUCCESS] new user registered {}".format(client))
            tcp_client.send(SUCCESS_MSG_02.encode(fmt))
            tcp_client.send("{}".format(client.client_id).encode(fmt))

        elif result.__class__.__name__ == 'VerificationData':
            client = verify_client(result.email, result.password)
            if client is not None:
                print('[SERVER][SUCCESS] user verified {} from {}'.format(client, address))
                tcp_client.send(SUCCESS_MSG_01.encode(fmt))
                tcp_client.send("{}".format(client.client_id).encode(fmt))
            else:
                print('[SERVER][FAILED] user was not verified from {}'.format(address))
                tcp_client.send(FAILURE_MSG_01.encode(fmt))
            
        elif result.__class__.__name__ == 'OrderData':
            order = insert_order(result.name, result.amount, result.client_id)
            print("[SERVER][SUCCESS] order registered {}".format(order))
            tcp_client.send(SUCCESS_MSG_02.encode(fmt))


    tcp_client.close()
        

server = create_tcp_server(socket.gethostbyname(socket.gethostname()), 5000)
establish_tcp_connection(server, 1000)


