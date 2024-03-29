import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# For Reconnecting Purpose
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen(1)

# List of sockets
sockets_list = [server_socket]
clients = {}


def receive_msg(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8"))

        return {
            "header": message_header,
            "data": client_socket.recv(message_length)
        }
    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_msg(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user

            print("Accepted New Connection from %s" % user['data'].decode("utf-8"))

        else:
            message = receive_msg(notified_socket)

            if message is False:
                print("Connection Closed")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print("Received Message from %s" % user["data"].decode("utf-8"))

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
