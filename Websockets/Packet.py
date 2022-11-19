class Packet:  # packet objects to store path data and node status data
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
    # we will make our packet size 42 bytes, this accommodates note State (42 bytes) and pathpoint (41 bytes)

    def packetType(self):
        if self.data[0:1] == b'1':
            return 1
        if self.data[0:1] == b'2':
            return 2


class node_state(Packet):  # packet to hold data for the node state
    def __init__(self, data):
        self.data = data
        self.__packet_size = 41
        self.heading = 0
        self.velocity = 0
        self.X = 0
        self.Y = 0
        self.ts_ms = 0
        self.State = 0
        # self.sizes = [2,2,2,]
        self.parseData()

    # __init__(self,data, heading, velocity, X, Y, ts_ms, State):
    #    self.data = data
    #    self.heading = heading
    #    self.velocity = velocity
    #    self.X = X
    #    self.Y = Y
    #    self.ts_ms = ts_ms
    #    self.State = State

    # TODO i believe python has a mechanism to iterate through an object's data properties sequentially.
    # So this function could probably be generalized and applied to the parent class instead?
    # it should make creating new packets easier that way
    # if the differing sizes is an issue, talk to me cause I have a few ideas

    #use this link: https://bobbyhadz.com/blog/python-iterate-over-object-attributes
    # only thing I can find is struct.unpack() but this would use the same format for the entire data packet i.e it would treat the whole packet at doubles or ints

    def parseData(self):  # method to parse the data packet and update packet arguments to match
        self.heading = self.data[0:8]  # heading angle relative to start (double - 8 bytes)
        self.velocity = self.data[8:16]  # current velocity (double - 8 bytes)
        self.X = self.data[16:24]  # Estimated x position relative to start (double - 8 bytes)
        self.Y = self.data[24:32]  # Estimated y position relative to start (double - 8 bytes)
        self.ts_ms = self.data[32:40]  # time stamp in ms since start (uint64_t - 8 bytes)
        self.State = self.data[40:41]  # byte enumeration of node executing state (char - 1 byte)


class path_packet(Packet):  # packet to hold data for path planning
    def __init__(self, data, x, y, ts_ms, v, heading):
        self.data = data
        self.packet_size = 40
        self.x = x
        self.y = y
        self.ts_ms = ts_ms
        self.v = v
        self.heading = heading
        self.parseData()

    def parseData(self):  # method to parse the data packet and update packet arguments to match
        # for attribute in dir(self):
        self.x = self.data[0:8]  # x position for path point (double - 8 bytes)
        self.y = self.data[8:16]  # y position for path point (double - 8 bytes)
        self.ts_ms = self.data[16:24]  # time stamp in ms of when this point should be hit (uint64_t - 8 bytes)
        self.v = self.data[24:32]  # velocity at this point (double - 8 bytes)
        self.heading = self.data[32:40]  # heading at this point (double - 8 bytes)

#
# class NodeManager:
#     def __init__(self, id, ws):
#         self.id = id
#         self.ws = ws


# one fsm branches between packet codes, sub FSM handles conversation back and forth between
# draw the FSM before coding
