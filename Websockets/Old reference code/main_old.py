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

    def convertData(self):
        if self.data[0] == 1: # char identifier = 1 means Node_state packet
            heading = self.data[1:65] # heading angle relative to start (double - 8 bytes)
            velocity = self.data[65:129] # current velocity (double - 8 bytes)
            X = self.data[129:193] # Estimated x position relative to start (double - 8 bytes)
            Y = self.data[193:257] # Estimated y position relative to start (double - 8 bytes)
            ts_ms = self.data[257:321] # time stamp in ms since start (uint64_t - 8 bytes)
            State = self.data[321:385] # byte enumeration of node executing state (char - 1 byte)

        if self.data[0] == 2: # char identifier = 2 means path packet
            x = self.data[1:65] # x position for path point (double - 8 bytes)
            y = self.data[65:129] # y position for path point (double - 8 bytes)
            ts_ms = self.data[129:193] # time stamp in ms of when this point should be hit (uint64_t - 8 bytes)
            v = self.data[193:257] # velocity at this point (double - 8 bytes)
            heading = self.data[257:321] # heading at this point (double - 8 bytes)

        else #return who am I state


class NodeManager:
    def __init__(self,id, ws):
        self.id = id
        self.ws = ws
    def SendState(self,):


class node_State(Packet):
    def __init__(self):


class path_Point(Packet):
    def __init__(self):

# one fsm branches between packet codes, sub FSM handles conversation back and forth between
# draw the FSM before coding