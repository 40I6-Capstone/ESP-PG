
# Node class to create 'node' objects for the server. This allows us to reference the nodes by their conn / address as well as store their current state
class Node:
    def __init__(self, conn, address, heading, velocity, X, Y, ts_ms, State):
        self.conn = conn # new socket object usable to send and receive data on the connection
        self.address = address # the address bound to the socket on the other end of the connection
        self.status_size = 5
        # Below values will store the current state of the node
        self.heading = heading
        self.velocity = velocity
        self.X = X
        self.Y = Y
        self.ts_ms = ts_ms
        self.State = State

    def updateState(self, Packet): # method to update the current state to match that of an incoming state packet
        self.heading = Packet.heading
        self.velocity = Packet.velocity
        self.X = Packet.X
        self.Y = Packet.Y
        self.ts_ms = Packet.ts_ms
        self.State = Packet.State
