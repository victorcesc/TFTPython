from message import Message


#simulando WRQ
message = bytearray()
message.append(0)
message.append(1)
opcode = message
buffer = bytearray()
buffer += 'filename'.encode('ascii')
buffer.append(0)
buffer += 'mode'.encode('ascii')
buffer.append(0)
print(buffer.decode('ascii'))
##teste = Message(opcode,buffer)
##print(Message.serialize(teste))