class Packet:  # packet objects to store path data and node status data
    def __init__(self, data):
        self.data__ = data

    # byte sizes for different data types:
    # char - 1
    # short - 2
    # int - 4
    # long - 8
    # long long - 8
    # double - 8 bytes
    # uint64_t - 8 bytes
    # we will make our packet size 42 bytes, this accommodates note State (42 bytes) and pathpoint (41 bytes)

    def parseData(self):
        index = 0
        # get list of all variables for an object
        variables = [variable for variable in vars(self)  # to exclude a variable from this list, use '__' at the beginning or end of the name
                     if not variable.startswith('__')
                     and not variable.endswith('__')]
        for attr in variables: # set the value for each variable from the passed in data based on its known size
            length = len(getattr(self, attr))
            setattr(self, attr, self.data__[index: index + length])
            # print('index', index)
            index = index + length
            # print(getattr(packet, attr), length)




class node_state(Packet):  # packet to hold data for the node state
    def __init__(self, data):
        self.data__ = data
        self.packet_size__ = 41
        # set all node state values to 0 by deafult
        self.x = b'00000000'
        self.y = b'00000000'
        self.velocity = b'00000000'
        self.heading = b'00000000'
        self.ts_ms = b'00000000'
        self.state = b'0'
        self.parseData() # automatically parse data when a new object is created


class path_packet(Packet):  # packet to hold data for path planning
    # TODO if we are passing in the data array, why does the constructor also take in the other values? it should be one or the other no?
    # TODO if you expect two different ways of creating this object (which i think is probably reasonable) then try to create "multiple constructors"
    # https://medium.com/@yourblogcoach1/multiple-constructors-in-python-97dac362a515
    def __init__(self, data, x, y, velocity, heading, ts_ms):
        self.data__ = data
        self.packet_size__ = 40
        self.x = x
        self.y = y
        self.velocity = velocity
        self.heading = heading
        self.ts_ms = ts_ms
        #TODO do you not want to automatically parse if the constructor has the data array passed into it?
        # self.parseData()