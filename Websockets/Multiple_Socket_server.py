#!usr/bin/python
import _thread
import socket
import sys
import Packet  # Packet class
import Node

# TODO you have alot of stuff printing or asking for input for when you were testing,
# you should make all of that condition so that this code can execute in a "production" or "testing" mode

# TODO if you notice alot of the same await and reply patterns in the conversations, feel free to write a sub class as an fsm for that and just reuse that code
# this will come in handy when we eventually have more conversations happening (unlikley in my mind)


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
    # TODO is there a sizeof() equivalent we can use incase the size of this data structure changes?
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

# FSM Pseudocode:
# - Server turns on and waits to register X number of clients
# - Register clients then enter IDLE state
# - From IDLE we can: manually request a node state, receive a node state packet, or send a path packet to a node

# TODO, not really a todo, but aron will handle managing multiple, add in asynch functionality but on a callback basis so this single calss runs nicer
# TODO - update server to handle multiple nodes asyncronously 
# TODO - implement way for idle state to receive packet and go straight to node_state_receive


# TODO Turn this into a "node manager" class that can be instantiated mutliple times as Aron's code establishes socket connections
# He will take care of dealing with multiple of these node managers himself too
# (take the socket in as a constructor argument, also take in a node ID)

# TODO right now you've written everything to handle multiple nodes in this one manager, instead make this an object that handles one node
def main():
    try:

        # Example path packet data
        x = b'15.10100'
        y = b'34.35000'
        ts_ms = b'10506789'
        v = b'2.300000'
        heading = b'19.12345'
        path = x + y + ts_ms + v + heading

        host = '10.0.0.187'
        port = 7890
        tot_socket = 1
        list_sock = []
        node_list = []
        node_index = 0
        state = 'REGISTER_CLIENT'
        while 1:
            match state:
                # TODO for this state, all you really need to do is 
                case 'REGISTER_CLIENT': 
                    print('********  REGISTER_CLIENT STATE  ********')
                    # TODO at this point Aron would have established the socket connection for you, and then passed it in alongside an ID
                    # this state just needs to send that ID back to the node and setup any callbacks if youre doing asynch stuff
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
                    # TODO cut the testing fluff or wrap it in some conditional for testing mode
                    print('********  IDLE STATE  ********')
                    selection = int(input('Enter 1 to request node state, 2 to send a path packet, 3 to check for a node state update: '))
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

                case 'REQUEST_NODE_STATE':
                    print('********  REQUEST_NODE_STATE STATE  ********')
                    node_list[node_index].conn.send(b'node')
                    state = 'NODESTATE_RECEIVE'

                # case 'NODESTATE_SEND':  # send a nodestate packet
                #     print('********  NODESTATE_SEND STATE  ********')
                #     node_list[node_index].conn.sendall(b'1')  # check 0th node by default, unless otherwise specified
                #     state = 'NODESTATE_RECEIVE'

                case 'NODESTATE_RECEIVE':  # wait for response from node, once received, parse the data, and update internal current state
                    print('********  NODESTATE_RECEIVE STATE  ********')
                    buffer = b''
                    # TODO directly get the size of how big this packet is, or make it a property of the packet itself that we change whenever the packet class changes
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
                    node_list[node_index].conn.sendall(b'path')
                    state = 'SENDPATH_AWAIT_REPLY'

                case 'SENDPATH_AWAIT_REPLY':  # wait for ready signal from node
                    print('********  SENDPATH_AWAIT_REPLY STATE  ********')
                    status = node_list[node_index].conn.recv(5)  #TODO Ideally this size is a property of the object too
                    if status == b'ready':
                        state = 'SENDPATH_SEND_STREAM'
                    # else:
                    #     state = 'IDLE'

                    # buffer = b''
                    # not_ready = True
                    # while not_ready:
                    #     while len(buffer) < 42:  # wait for the buffer to fill with packet data
                    #         data = node_list[node_index].conn.recv(42)  # packet size of 42 bytes for state
                    #         buffer += data
                    #     if buffer[0:1] == b'3':  # assume first byte being 3 means 'ready' for now
                    #         not_ready = False


                case 'SENDPATH_SEND_STREAM':  # SEND STREAM OF BYTES FOR PATH
                    print('********  SENDPATH_SEND_STREAM STATE  ********')
                    # TODO: path_packet needs to be filled with data received from openCV and path planning algorithm, for now it is left empty
                    path_packet = Packet.path_packet(0,0,0,0,0,0)
                    path_packet.data = path
                    node_list[node_index].conn.sendall(path_packet.data)
                    state = 'SENDPATH_AWAIT_CHECK'

                case 'SENDPATH_AWAIT_CHECK':  # wait for packet received from node
                    print('********  SENDPATH_AWAIT_CHECK STATE  ********')
                    status = node_list[node_index].conn.recv(4)
                    if status == b'good':
                        state = 'IDLE'
                    elif status == b'nope':
                        print('path packet not received properly, trying again')
                        state = 'SENDPATH_AWAIT_REPLY'
                    else:
                        raise Exception("error encountered in sending path")

                    # buffer = b''
                    # packet_not_received = True
                    # while packet_not_received:
                    #     while len(buffer) < 42:  # wait for the buffer to fill with packet data
                    #         data = node_list[node_index].conn.recvall(42)  # packet size of 42 bytes for state
                    #         buffer += data
                    #     if buffer[0:1] == b'4':  # assume first byte being 4 means 'packet received' for now
                    #         packet_not_received = False
                    #         state = 'IDLE'
                    #     if buffer[0:1] == b'5':  # assume first byte being 5 means 'packet not properly received' for now
                    #         state = 'SENDPATH_SEND_STREAM'
                    #         break

    except KeyboardInterrupt as msg:
        sys.exit(0)


if __name__ == "__main__":
    main()
