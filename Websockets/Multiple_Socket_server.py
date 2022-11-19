#!usr/bin/python
import _thread
import socket
import sys
import Packet  # Packet class
import Node


def clientthread(conn):  # set up a new client thread
    buffer = b''
    while True:
        data = conn.recv(8192)
        buffer += data
        print(buffer)
    # conn.sendall(reply)
    conn.close()


def request_state(Node, datasize):
    buffer = b''
    while len(buffer) < datasize:  # wait for the buffer to fill with packet data
        data = Node.conn.recv(datasize)  # packet size of 42 bytes for state
        buffer += data
        print(buffer)
    packet = Packet.node_state(buffer)
    packet.parseData()  # parse the received data
    Node.updateState(packet)
    return packet


def send_path(path_packet, Node):
    Node.conn.sendall(path_packet.data)


# FSM Pseudocode:
# - Server turns on and waits to register X number of clients
# - Register clients then enter IDLE state
# - From IDLE we can: manually request a node state, receive a node state packet, or send a path packet to a node

# TODO, not really a todo, but aron will handle managing multiple, add in asynch functionality but on a callback basis so this single calss runs nicer

# TODO Turn this into a "node manager" class that can be instantiated mutliple times as Aron's code establishes socket connections
# He will take care of dealing with multiple of these node managers himself too
# (take the socket in as a constructor argument, also take in a node ID)

# TODO right now you've written everything to handle multiple nodes in this one manager, instead make this an object that handles one node
def server(sock,nodeID): #take in socket and nodeID as arguments
    mode = 'testing'
    # mode = production
    try:

        # Example path packet data
        x = b'15.10100'
        y = b'34.35000'
        ts_ms = b'10506789'
        v = b'2.300000'
        heading = b'19.12345'
        path = x + y + ts_ms + v + heading

        host = '192.168.0.57'
        port = 7890
        tot_socket = 1 # total number of sockets that we are connecting to
        list_sock = []
        node_list = []
        node_index = 0
        state = 'REGISTER_CLIENT'
        while 1:
            match state:
                case 'REGISTER_CLIENT':
                    # TODO at this point Aron would have established the socket connection for you, and then passed it in alongside an ID
                    # this state just needs to send that ID back to the node and setup any callbacks if youre doing asynch stuff
                    # thus, wrap any socket connection stuff in testing condition
                    if mode == 'testing': # testing or production mode
                        print('********  REGISTER_CLIENT STATE  ********')
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
                                node = Node.Node(conn, addr, 0, 0, 0, 0, 0, 0)
                                # node.conn = conn
                                # node.address = addr
                                node_list.append(node)
                                # _thread.start_new_thread(clientthread, (conn,))
                    if mode == 'production':
                        state = 'IDLE'
                        # TODO - values passed in from Aron for socket and ID go here

                    state = 'IDLE'

                case 'IDLE':  # wait for function call or a request from the network
                    if mode == 'testing':
                        print('********  IDLE STATE  ********')
                        selection = int(input(
                            'Enter 1 to request node state, 2 to send a path packet, 3 to check for a node state update: '))
                        if selection == 1:
                            state = 'REQUEST_NODE_STATE'
                        elif selection == 2:
                            state = 'SEND_PATH_PACKET'
                        elif selection == 3:
                            for i in range(len(node_list)):  # check all nodes to see if they sent data
                                received_data = node_list[i].conn.recv(4)
                                if received_data:
                                    node_index = i
                                    if received_data == b'node':  # checks if we are receiving a node state packet, this can be changed to a 1 later to save data
                                        state = 'NODESTATE_RECEIVE'
                                    elif received_data == b'path':
                                        state = 'SEND_PATH_PACKET'
                                    break
                        else:
                            print('Invalid Selection')
                    if mode == 'production':
                        # TODO - wait for function call from Aron or a request from the network

                case 'REQUEST_NODE_STATE':
                    if mode == 'testing':
                        print('********  REQUEST_NODE_STATE STATE  ********')
                    node_list[node_index].conn.send(b'node')
                    state = 'NODESTATE_RECEIVE'


                case 'NODESTATE_RECEIVE':  # wait for response from node, once received, parse the data, and update internal current state
                    if mode == 'testing':
                        print('********  NODESTATE_RECEIVE STATE  ********')
                    buffer = b''
                    node_state_packet = Packet.node_state(buffer)
                    while len(buffer) < node_state_packet.packet_size:  # wait for the buffer to fill with packet data
                        data = node_list[node_index].conn.recv(node_state_packet.packet_size)  # packet size of 42 bytes for state
                        buffer += data
                        print(buffer)
                    node_state_packet.data = buffer
                    node_state_packet.parseData()  # parse the received data
                    node_list[node_index].updateState(node_state_packet)
                    print('[*] received and parsed packet ')
                    state = 'IDLE'

                case 'SEND_PATH_PACKET':  # parse received data and update internal current state
                    if mode == 'testing':
                        print('********  SEND_PATH_PACKET STATE  ********')
                    node_list[node_index].conn.sendall(b'path')
                    state = 'SENDPATH_AWAIT_REPLY'

                case 'SENDPATH_AWAIT_REPLY':  # wait for ready signal from node
                    if mode == 'testing':
                        print('********  SENDPATH_AWAIT_REPLY STATE  ********')
                    status = node_list[node_index].conn.recv(5)  # TODO Ideally this size is a property of the object too
                    if status == b'ready':
                        state = 'SENDPATH_SEND_STREAM'

                case 'SENDPATH_SEND_STREAM':  # SEND STREAM OF BYTES FOR PATH
                    if mode == 'testing':
                        print('********  SENDPATH_SEND_STREAM STATE  ********')
                    # TODO: path_packet needs to be filled with data received from openCV and path planning algorithm, for now it is left empty
                    path_packet = Packet.path_packet(0, 0, 0, 0, 0, 0)
                    path_packet.data = path
                    node_list[node_index].conn.sendall(path_packet.data)
                    state = 'SENDPATH_AWAIT_CHECK'

                case 'SENDPATH_AWAIT_CHECK':  # wait for packet received from node
                    if mode == 'testing':
                        print('********  SENDPATH_AWAIT_CHECK STATE  ********')
                    status = node_list[node_index].conn.recv(4)
                    if status == b'good':
                        state = 'IDLE'
                    elif status == b'nope':
                        print('path packet not received properly, trying again')
                        state = 'SENDPATH_AWAIT_REPLY'
                    else:
                        raise Exception("error encountered in sending path")

    except KeyboardInterrupt as msg:
        sys.exit(0)


if __name__ == "__server__":
    server()
