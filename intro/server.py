import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 1234 is PORT where to listen
s.bind((socket.gethostname(), 125))
s.listen(5)

print(socket.gethostname())

while True:
    clientsocket, address = s.accept()
    print(address)
    print("Connection has been established!")
    clientsocket.send(bytes("Welcome to the Server!"))
    clientsocket.close()
