import socket
import struct


from data import Data
from request import Request


UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MENSAGEM = b"recebido"

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


f = open("mesg_demos/teste","wb")

dados = "localhost\r\nlocalhost\r\n191.36.8.55\tlased\r\n191.36.8.55\tinet.sj.ifsc.edu.br\tinet\r\n191.36.9.247     opiap\r\n192.168.10.235  mk\r\n192.168.10.234  base\r\n10.1.10.200  baseac\r\n10.1.20.200  clienteac\r\n10.1.10.1  wom1ac # base\r\n10.1.20.1  wom2ac #cliente\r\n\r\n# The following lines are desirable for IPv6 capable hosts\r\n::1     localhost ip6-localhost ip6-loopback\r\nff02::1 ip6-allnodes\r\nff02::2 ip6-allrouters\r\n10.0.10.20 cliente1\r\n10.0.20.20 cliente2\r\n10.0.30.20 cliente3\r\n10.0.40.20 cliente4\r\n10.0.50.20 cliente5\r\n10.0.60.20191.36.8.55\tlased\r\n191.36.8.55\tinet.sj.ifsc.edu.br\tinet\r\n191.36.9.247     opiap\r\n192.168.10.235  mk\r\n192.168.10.234  base\r\n10.1.10.200  baseac\r\n10.1.20.200  clienteac\r\n10.1.10.1  wom1ac # base\r\n10.1.20.1  wom2ac #cliente\r\n\r\n# The following lines are desirable for IPv6 capable hosts\r\n::1     localhost ip6-localhost ip6-loopback\r\nff02::1 ip6-allnodes\r\nff02::2 ip6-allrouters\r\n10.0.10.20 cliente1\r\n10.0.20.20 cliente2\r\n10.0.30.20 cliente3\r\n10.0.40.20 cliente4\r\n10.0.50.20 cliente5\r\n10.0.60.20".encode('ascii')
 #dados = "victor asifpoaufouahjfnpuoawhnfpouafhnpoawufnpuioawnfuopawnfpuoawfnopiuawbnfiopawfhnuiopawfhnpaouiwfnpuawiohfnpioawfhniopuawhnfiopawhnfioawnfhiopawhnfa".encode('ascii')

f.write(dados)
f.close()

f2 = open("mesg_demos/teste","rb")

b = 1
rrq = Request(2,'host','netascii')
rrq = rrq.serialize()
# sock.sendto(rrq, (UDP_IP,UDP_PORT))

# data_r, addr = sock.recvfrom(512)
# print("received message: %s" % data_r)

while True:
    
    data_r, addr = sock.recvfrom(512) # buffer size is 1024 bytes
    print("received message: %s" % data_r)
    print(addr)
    
    dados = f2.read(512)
    block = struct.pack(">H",b)    
    data_t  = Data(3,block,dados) #ack
    data_t = data_t.serialize()
    print(len(data_t))
    
    b = b + 1
    if dados:  
        print("enviando %s" % data_t) 
        sock.sendto(data_t, addr)
    else :
        print("Arquivo acabou")
        b = 0
        break
 