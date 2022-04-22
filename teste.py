first = 0b01010101
second = 0b11110000


teste = 1
opcode = b'0000000000000001'

#concatenar bytes

buffer = bytearray()
buffer += opcode
buffer += 'filename'.encode('ascii')
#b += filename.encode('ascii')
buffer.append(0)
buffer += 'mode'.encode('ascii')
buffer.append(0)

print(buffer)