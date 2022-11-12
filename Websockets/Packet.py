class Packet:
    def __init__(self, data):
        self.data = data

    # byte sizes for different data types:
    # char - 1
    # short - 2
    # int - 4
    # long - 8
    # long long - 8
    # double - 8 bytes
    # uint64_t - 8 bytes
    # we will make our packet size 42 bytes, this accomodates note State (42 bytes) and pathpoint (41 bytes)
    def packetType(self):
        if self.data[0:1] == b'1':
            return 1
        if self.data[0:1] == b'2':
            return 2


class node_State(Packet):
    def __init__(self,data, heading, velocity, X, Y, ts_ms, State):
        self.data = data
        self.heading = heading
        self.velocity = velocity
        self.X = X
        self.Y = Y
        self.ts_ms = ts_ms
        self.State = State
    def convertData(self):
        self.heading = self.data[1:9] # heading angle relative to start (double - 8 bytes)
        self.velocity = self.data[9:17] # current velocity (double - 8 bytes)
        self.X = self.data[17:25] # Estimated x position relative to start (double - 8 bytes)
        self.Y = self.data[25:33] # Estimated y position relative to start (double - 8 bytes)
        self.ts_ms = self.data[33:41] # time stamp in ms since start (uint64_t - 8 bytes)
        self.State = self.data[41:42] # byte enumeration of node executing state (char - 1 byte)


class path_packet(Packet):
     def __init__(self, x, y, ts_ms, v, heading):
         self.x = x
         self.y = y
         self.ts_ms = ts_ms
         self.v = v
         self.heading = heading
     def convertData(self):
         self.x = self.data[1:9]  # x position for path point (double - 8 bytes)
         self.y = self.data[9:17]  # y position for path point (double - 8 bytes)
         self.ts_ms = self.data[17:25]  # time stamp in ms of when this point should be hit (uint64_t - 8 bytes)
         self.v = self.data[25:33]  # velocity at this point (double - 8 bytes)
         self.heading = self.data[33:41]  # heading at this point (double - 8 bytes)
#
# class NodeManager:
#     def __init__(self, id, ws):
#         self.id = id
#         self.ws = ws





# one fsm branches between packet codes, sub FSM handles conversation back and forth between
# draw the FSM before coding