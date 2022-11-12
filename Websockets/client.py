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
    host = '10.0.0.187'
    port = 7890
    # example Data for node_state:

    Heading = b'30.64000'
    Velocity = b'5.145000'
    X = b'2.980000'
    Y = b'103.5000'
    ts_ms = b'10.00000'
    State = b'1'
    data = Heading+Velocity+X+Y+ts_ms+State
    state_packet = Packet.Packet(data)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        heading = b'1'
        s.sendall(heading[0:1])
        time.sleep(3)
        s.sendall(state_packet.data)
        output = s.recv(1024)
    print('Received: ', repr(output))

asyncio.get_event_loop().run_until_complete(test())


#

