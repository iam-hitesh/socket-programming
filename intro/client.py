import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# socket.gethostname() is for local machine, can refer public IP or Local IP
# 1234 is PORT
s.connect((socket.gethostname(), 125))

full_msg = ''
while True:
    # Recieve only 10 bytes in one time.
    msg = s.recv(10)
    if len(msg) <= 0:
        break

    full_msg += msg

print(full_msg.decode("utf-8"))
