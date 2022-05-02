from message import Message
from request import Request


#simulando WRQ
# message = bytearray()
# message.append(0)
# message.append(1)
# opcode = message
# buffer = bytearray()
# buffer += 'filename'.encode('ascii')
# buffer.append(0)
# buffer += 'mode'.encode('ascii')
# buffer.append(0)
# print(buffer.decode('ascii'))
filename = 'oi.txt'
mode = 'NetAscii'

opcode = 2
buffer = bytearray()
buffer.append(0)
buffer.append(opcode)
buffer += filename.encode('ascii')
buffer.append(0)
buffer += mode.encode('ascii')
buffer.append(0)

print(buffer)
print("teste")
message = Message(buffer)
#print(message.getOpcode())
# print(message.serialize())
request = Request(2,'teste.txt','NetAscii')
print(request.serialize())


##teste = Message(opcode,buffer)
##print(Message.serialize(teste))