#!usr/bin/python
import _thread
import socket
import sys
import Packet  # Packet class
import Node


def clientthread(conn):
    buffer = b''
    while True:
        data = conn.recv(8192)
        buffer += data
        print(buffer)
    # conn.sendall(reply)
    conn.close()


def request_state(Node):
    Node.conn.sendall(b'1')  # send a 1 to indicate that we want node state
    buffer = b''
    while len(buffer) < 42:
        data = conn.recvall(42)  # packet size of 42 bytes for state
        buffer += data
        print(buffer)
    packet = Packet()
    packet.convertData() # parse the received data
    Node.updateState(packet)
    return packet

def send_path(path_packet,Node):
    Node.conn.sendall(path_packet.data)

def main():
    try:
        host = '10.0.0.187'
        port = 7890
        tot_socket = 2
        list_sock = []
        node_list = []
        for i in range(tot_socket):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port + i))
            s.listen(10)
            list_sock.append(s)
            print("[*] Server listening on %s %d" % (host, (port + i)))


        while 1:
            for j in range(len(list_sock)):
                conn, addr = list_sock[j].accept()
                print('[*] Connected with ' + addr[0] + ':' + str(addr[1]))
                node = Node()
                node.conn = conn
                node.address = addr
                node_list.append(node)
                _thread.start_new_thread(clientthread, (conn,))
        s.close()

    except KeyboardInterrupt as msg:
        sys.exit(0)


if __name__ == "__main__":
    main()
