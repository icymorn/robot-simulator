import socket
import time

HOST = '127.0.0.1'    # The remote host
PORT = 9556              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    str = raw_input("#number value")
    if len(str) > 2:
        s.sendall(str)
    else:
        break
s.close()