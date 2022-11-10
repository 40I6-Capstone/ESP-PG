import struct
# heading = b'5.1'
# struct_heading = struct.pack("f", heading)
# byte_heading = bytearray(struct.pack("f", heading))
# print(struct_heading)

# example Data for node_state:
# for a bytes or bytearray object b, b[0] will be an integer representing the ASCII value of single bytes, while b[0:1] will be a bytes or bytearray object of length 1
Heading = b'30.64000'
Velocity = b'5.145000'
X = b'2.980000'
Y = b'103.5'
ts_ms = b'1000'
State = b'1'
data = [Heading,Velocity,X,Y,ts_ms,State]
test = b'1'+ Heading + Velocity + X
print(test)
print(type(data))
print(type(Heading))
print(len(Heading))
print(Heading[0:1])

H = test[1:9]

# Heading = 25.5
# Velocity = 5.145
# X = 2.98
# Y = 103.5
# ts_ms = 1000
# State = 1
# byte_data = bytearray(data)
# print(byte_data)