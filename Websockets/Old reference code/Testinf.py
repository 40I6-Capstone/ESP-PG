import struct
import Packet
# heading = b'5.1'
# struct_heading = struct.pack("f", heading)
# byte_heading = bytearray(struct.pack("f", heading))
# print(struct_heading)




# example Data for node_state:
# for a bytes or bytearray object b, b[0] will be an integer representing the ASCII value of single bytes, while b[0:1] will be a bytes or bytearray object of length 1
# example Data for current node_state:
heading = b'30.64000'
velocity = b'5.145000'
x = b'2.980000'
y = b'103.5000'
ts_ms = b'10.00000'
state = b'1'
data = heading + velocity + x + y + ts_ms + state
print(data)
print(type(data))
packet = Packet.node_state(data)
print(vars(packet))
packet.parseData()
print(vars(packet))
# variables = [variable for variable in vars(packet)
#         if not variable.startswith('__')
#         and not variable.endswith('__')]
# print(variables)
# packet.x = x
# index = 0
# for attr in variables:
#     length = len(getattr(packet, attr))
#     try:
#         setattr(packet,attr,data[index : index+length])
#         print('index',index)
#         index = index + length
#         print(getattr(packet, attr),length)
#     except:
#         print(getattr(packet, attr), 0)

#               and not attribute.endswith('__')]
# attributes = [attribute for attribute in dir(packet)
#               if not attribute.startswith('__')
#               and not attribute.endswith('__')]
# print(attributes)
# index = 0
# for attr in attributes:
#     # cls_id employee
#     # name bobbyhadz
#     # salary 100
#     # print(attr,)
#     print(attr, getattr(packet, attr))
# test = b'1'+ Heading + Velocity + X
# length = [1]
# print(range(len(length)-1))
#
# # Example path packet data
# x = b'15.10100'
# y = b'34.35000'
# ts_ms = b'10506789'
# v = b'2.300000'
# heading = b'19.12345'
# path = x + y + ts_ms + v + heading
# print(path)
# print(type(path))

