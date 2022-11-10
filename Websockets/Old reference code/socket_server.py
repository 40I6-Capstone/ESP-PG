# Echo server program
import socket

HOST = '10.0.0.187'                 # Symbolic name meaning all available interfaces
PORT = 7890             # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(2) # listen for this number of connections MAX
    conn, addr = s.accept()
    with conn:
        print('Connected by', conn)
        print('Address: ', addr[1])
        while True:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(data)