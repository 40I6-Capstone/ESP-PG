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
        data = Node.conn.recv(42)  # packet size of 42 bytes for state
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
        tot_socket = 1
        list_sock = []
        node_list = []
        node_index = 0
        state = 'REGISTER_CLIENT'
        while 1:
            match state:
                case 'REGISTER_CLIENT':
                    for i in range(tot_socket):
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        s.bind((host, port + i))
                        s.listen(10)
                        list_sock.append(s)
                        print("[*] Server listening on %s %d" % (host, (port + i)))
                    while len(node_list) < tot_socket:
                        for j in range(len(list_sock)):
                            conn, addr = list_sock[j].accept()
                            print('[*] Connected with ' + addr[0] + ':' + str(addr[1]))
                            node = Node.Node(conn,addr,0,0,0,0,0,0)
                            # node.conn = conn
                            # node.address = addr
                            node_list.append(node)
                            # _thread.start_new_thread(clientthread, (conn,))
                    # s.close()
                    state = 'IDLE'

                case 'IDLE':  # wait for function call or a request from the network
                    print('********  IDLE STATE  ********')
                    for i in range(len(node_list)): # check all nodes to see if they sent data
                        received_data = node_list[i].conn.recv(1)
                        if received_data:
                            node_index = i
                            if received_data[0:1] == b'1':
                                state = 'NODESTATE_RECEIVE'
                            elif received_data[0:1] == b'2':
                                state = 'SEND_PATH_PACKET'
                        break

                case 'NODESTATE_SEND':  # send a nodestate packet
                    print('********  NODESTATE_SEND STATE  ********')
                    node_list[node_index].conn.sendall(b'1')  # check 0th node by default, unless otherwise specified
                    state = 'NODESTATE_RECEIVE'

                case 'NODESTATE_RECEIVE':  # wait for response from node, once received, parse the data, and update internal current state
                    print('********  NODESTATE_RECEIVE STATE  ********')
                    buffer = b''
                    while len(buffer) < 41:  # wait for the buffer to fill with packet data
                        data = node_list[node_index].conn.recv(42)  # packet size of 42 bytes for state
                        buffer += data
                        print(buffer)
                    node_state_packet = Packet.node_State(buffer,0,0,0,0,0,0)
                    node_state_packet.convertData()  # parse the received data
                    node_list[node_index].updateState(node_state_packet)
                    print('[*] received and parsed packet ')
                    state = 'IDLE'

                case 'SEND_PATH_PACKET':  # parse received data and update internal current state
                    print('********  SEND_PATH_PACKET STATE  ********')
                    Node.conn.sendall(b'2')
                    state = 'SENDPATH_AWAIT_REPLY'

                case 'SENDPATH_AWAIT_REPLY':  # wait for ready signal from node
                    print('********  SENDPATH_AWAIT_REPLY STATE  ********')
                    buffer = b''
                    not_ready = True
                    while not_ready:
                        while len(buffer) < 42:  # wait for the buffer to fill with packet data
                            data = Node.conn.recv(42)  # packet size of 42 bytes for state
                            buffer += data
                        if buffer[0:1] == b'3':  # assume first byte being 3 means 'ready' for now
                            not_ready = False
                    state = 'SENDPATH_SEND_STREAM'

                case 'SENDPATH_SEND_STREAM':  # SEND STREAM OF BYTES FOR PATH
                    print('********  SENDPATH_SEND_STREAM STATE  ********')
                    # how do I take in path point data for this?
                    path_packet = Packet()
                    send_path(path_packet, Node)
                    state = 'SENDPATH_AWAIT_CHECK'

                case 'SENDPATH_AWAIT_CHECK':  # wait for packet received from node
                    print('********  SENDPATH_AWAIT_CHECK STATE  ********')
                    buffer = b''
                    packet_not_received = True
                    while packet_not_received:
                        while len(buffer) < 42:  # wait for the buffer to fill with packet data
                            data = Node.conn.recvall(42)  # packet size of 42 bytes for state
                            buffer += data
                        if buffer[0:1] == b'4':  # assume first byte being 4 means 'packet received' for now
                            packet_not_received = False
                            state = 'IDLE'
                        if buffer[0:1] == b'5':  # assume first byte being 5 means 'packet not properly received' for now
                            state = 'SENDPATH_SEND_STREAM'
                            break

    except KeyboardInterrupt as msg:
        sys.exit(0)


if __name__ == "__main__":
    main()
