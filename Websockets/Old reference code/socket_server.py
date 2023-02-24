# Echo server program
import socket

HOST = '192.168.2.23'                 # Symbolic name meaning all available interfaces
PORT = 7890             # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1) # listen for this number of connections MAX
    conn, addr = s.accept()
    with conn:
        print('Connected by', conn)
        print('Address: ', addr[1])
        while True:
            msg = input() + '\n'
            conn.send(msg.encode())
            # conn.send(b'node')
            # data = conn.recv(8)
            # print(type(data))
            # print(data)
            # if not data: break
            # conn.sendall(data)