import websockets
import socket
import asyncio
import warnings
import struct
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        heading = b'5.01'
        s.sendall(heading[0:1])
        #s.sendall(b'Hello,world')
        data = s.recv(1024)
    print('Received: ', repr(data))

asyncio.get_event_loop().run_until_complete(test())

# example Data for node_state:
Heading = 25.5
Velocity = 5.145
X = 2.98
Y = 103.5
ts_ms = 1000
State = 1

data = [Heading,Velocity,X,Y,ts_ms,State]
