import Packet

class Node:
    def __init__(self, conn, address, heading, velocity, X, Y, ts_ms, State):
        self.conn = conn
        self.address = address
        self.heading = heading
        self.velocity = velocity
        self.X = X
        self.Y = Y
        self.ts_ms = ts_ms
        self.State = State

    def updateState(self, Packet):
        self.heading = Packet.heading
        self.velocity = Packet.velocity
        self.X = Packet.X
        self.Y = Packet.Y
        self.ts_ms = Packet.ts_ms
        self.State = Packet.State
