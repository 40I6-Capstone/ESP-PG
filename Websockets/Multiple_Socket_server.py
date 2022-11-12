#!usr/bin/python
import _thread
import socket
import sys
import Packet  # Packet class
import Node


def clientthread(conn): # set up a new client thread
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
    while len(buffer) < 42:  # wait for the buffer to fill with packet data
        data = Node.conn.recvall(42)  # packet size of 42 bytes for state
        buffer += data
        print(buffer)
    packet = Packet()
    packet.data = buffer
    packet.convertData()  # parse the received data
    Node.updateState(packet)
    return packet


def send_path(path_packet, Node):
    Node.conn.sendall(path_packet.data)


def main():
    try:
        host = '10.0.0.187'
        port = 7890
        tot_socket = 2
        list_sock = []
        node_list = []
        node_index = 0
        state = 'REGISTER_CLIENT'

        match state:
            case 'REGISTER_CLIENT':
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
                # s.close()
                state == 'IDLE'

            case 'IDLE':  # wait for function call or a request from the network
                print('waiting 10 seconds for user input, if no option is selected, node state will be requested')
                print('Select Node 1 or 2')
                # maybe use python input() here? but I don't think that is the best way


            case 'NODESTATE_SEND':  # send a nodestate packet
                node_list[node_index].conn.sendall(b'1')  # check 0th node by default, unless otherwise specified
                state = 'NODESTATE_RECEIVE'

            case 'NODESTATE_RECEIVE':  # wait for response from node, once received, parse the data, and update internal current state
                buffer = b''
                while len(buffer) < 42:  # wait for the buffer to fill with packet data
                    data = Node.conn.recvall(42)  # packet size of 42 bytes for state
                    buffer += data
                    print(buffer)
                packet = Packet()
                packet.data = buffer
                packet.convertData()  # parse the received data
                Node.updateState(packet)
                state = 'IDLE'

            case 'SEND_PATH_PACKET':  # parse received data and update internal current state
                Node.conn.sendall(b'2')
                state = 'SENDPATH_AWAIT_REPLY'

            case 'SENDPATH_AWAIT_REPLY':  # wait for ready signal from node
                buffer = b''
                not_ready = True
                while not_ready:
                    while len(buffer) < 42:  # wait for the buffer to fill with packet data
                        data = Node.conn.recvall(42)  # packet size of 42 bytes for state
                        buffer += data
                    if buffer[0] == b'3':  # assume first byte being 3 means 'ready' for now
                        not_ready = False
                state = 'SENDPATH_SEND_STREAM'

            case 'SENDPATH_SEND_STREAM':  # SEND STREAM OF BYTES FOR PATH
                # how do I take in path point data for this?
                path_packet = Packet()
                send_path(path_packet, Node)
                state = 'SENDPATH_AWAIT_CHECK'

            case 'SENDPATH_AWAIT_CHECK':  # wait for packet received from node
                buffer = b''
                packet_not_received = True
                while packet_not_received:
                    while len(buffer) < 42:  # wait for the buffer to fill with packet data
                        data = Node.conn.recvall(42)  # packet size of 42 bytes for state
                        buffer += data
                    if buffer[0] == b'4':  # assume first byte being 4 means 'packet received' for now
                        packet_not_received = False
                        state = 'IDLE'
                    if buffer[0] == b'5':  # assume first byte being 5 means 'packet not properly received' for now
                        state = 'SENDPATH_SEND_STREAM'
                        break

    except KeyboardInterrupt as msg:
        sys.exit(0)


if __name__ == "__main__":
    main()
