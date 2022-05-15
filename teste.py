from http import server
import os
import struct
from message import Message
from request import Request
from data import Data



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
# filename = 'oi.txt'
# mode = 'NetAscii'

# opcode = 2
# buffer = bytearray()
# print("oie")
# print(len(buffer))
# buffer.append(0)
# buffer.append(opcode)
# print("opcode")
# print(len(buffer))

# buffer += filename.encode('ascii')
# buffer.append(0)
# buffer += mode.encode('ascii')
# buffer.append(0)

# print(buffer)
# print("teste")
# message = Message(buffer)



# #print(message.getOpcode())
# # print(message.serialize())
# request = Request(2,'teste.txt','NetAscii')
# request.serialize()
# #print(request.serialize())

# file = open("mesg_demos/data","rb")
# #print(file.read(512))
# print(os.path.getsize("mesg_demos/data"))

# pt = file.read(508)
# pt2 = file.read(350)
# pt3 = file.read(200)


# print("opa: ")
# print(pt)


# if pt3:
#     print("receba")

# block = 127
# block = struct.pack(">H",block)
# dados = "".encode('ascii')

# data = Data(3,block,pt)
dados = "localhost\r\nlocalhost\r\n191.36.8.55\tlased\r\n191.36.8.55\tinet.sj.ifsc.edu.br\tinet\r\n191.36.9.247     opiap\r\n192.168.10.235  mk\r\n192.168.10.234  base\r\n10.1.10.200  baseac\r\n10.1.20.200  clienteac\r\n10.1.10.1  wom1ac # base\r\n10.1.20.1  wom2ac #cliente\r\n\r\n# The following lines are desirable for IPv6 capable hosts\r\n::1     localhost ip6-localhost ip6-loopback\r\nff02::1 ip6-allnodes\r\nff02::2 ip6-allrouters\r\n10.0.10.20 cliente1\r\n10.0.20.20 cliente2\r\n10.0.30.20 cliente3\r\n10.0.40.20 cliente4\r\n10.0.50.20 cliente5\r\n10.0.60.20191.36.8.55\tlased\r\n191.36.8.55\tinet.sj.ifsc.edu.br\tinet\r\n191.36.9.247     opiap\r\n192.168.10.235  mk\r\n192.168.10.234  base\r\n10.1.10.200  baseac\r\n10.1.20.200  clienteac\r\n10.1.10.1  wom1ac # base\r\n10.1.20.1  wom2ac #cliente\r\n\r\n# The following lines are desirable for IPv6 capable hosts\r\n::1     localhost ip6-localhost ip6-loopback\r\nff02::1 ip6-allnodes\r\nff02::2 ip6-allrouters\r\n10.0.10.20 cliente1\r\n10.0.20.20 cliente2\r\n10.0.30.20 cliente3\r\n10.0.40.20 cliente4\r\n10.0.50.20 cliente5\r\n10.0.60.20".encode('ascii')

server_f = open("host","rb")

s = server_f.read()

size = os.path.getsize("host")
print(size)
print(s.decode() == dados.decode())


# test = data.serialize()
# file_t = open("mesg_demos/teste_data","wb")
# file_t.write(test)
# file_t.close()
# file = open("mesg_demos/teste_data","rb")
# print(test)
# print(len(test))
# print(os.path.getsize("mesg_demos/teste_data"))
#print(type(test[2]))

#print(sys.getsizeof(data.serialize()))



##teste = Message(opcode,buffer)
##print(Message.serialize(teste))