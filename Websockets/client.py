# import websockets
import socket
import asyncio
import warnings
import struct
import Packet
import Node
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)  #ignore deprecation warnings

async def listen(): #websocket library test
    url = "ws://172.21.48.1:7890" #this is the local machine ip address with the port number
    async with websockets.connect(url) as ws: #connect to the server
        await ws.send("Hello Server!") #Send a greeting message
        # stay alive forever listening for messages
        while True:
            msg = await ws.recv()
            print(msg)

async def test(): #socket library test

    # example Data for current node_state:
    Heading = b'30.64000'
    Velocity = b'5.145000'
    X = b'2.980000'
    Y = b'103.5000'
    ts_ms = b'10.00000'
    State = b'1'
    data = Heading+Velocity+X+Y+ts_ms+State
    state_packet = Packet.Packet(data)

#   FSM for client
    state = 'IDLE'

    print('********  CONNECT STATE  ********')
    host = '192.168.0.57'
    port = 7890
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print('[*] Connected to Server')

        while 1: # Run FSM forever
            match state:
                case 'CONNECT':
                    print('********  CONNECT STATE  ********')
                    host = '10.0.0.187'
                    port = 7890
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((host, port))
                        print('[*] Connected to Server')
                    state = 'IDLE'

                case 'IDLE':
                    print('********  IDLE STATE  ********')
                    received_data = s.recv(4)
                    if received_data == b'node':
                        state = 'SEND_STATE'
                    elif received_data == b'path':
                        state = 'PATH_ALLOCATION'

                case 'SEND_STATE':
                    print('********  SEND_STATE STATE  ********')
                    s.sendall(state_packet.data)
                    state = 'IDLE'

                case 'PATH_ALLOCATION':
                    print('********  PATH_ALLOCATION STATE  ********')
                    new_path = Packet.path_packet(0,0,0,0,0,0)
                    s.sendall(b'ready')
                    state = 'PATH_RECEIVE'

                case 'PATH_RECEIVE':
                    print('********  PATH_RECEIVE STATE  ********')
                    new_path.data = s.recv(40)
                    new_path.parseData() # convert packet data to update current path data
                    state = 'RESPOND_CHECK'

                case 'RESPOND_CHECK':
                    print('********  RESPOND_CHECK STATE  ********')
                    if new_path.data != 0:
                        s.sendall(b'good')
                        state = 'IDLE'
                    else:
                        s.sendall(b'nope')
                        state = 'PATH_ALLOCATION'





asyncio.get_event_loop().run_until_complete(test())


#

