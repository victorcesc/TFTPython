import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MENSAGEM = b"recebido"

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)
    sock.sendto(ACK, addr)

 # recebe uma mensagem tipo ?ACK_0 / !DATA_N
        # if msg[1] == 4:
        #     if self.mode == 'NetAscii':
        #         f = open(self.datafile)
        #         max_n = self.max_n
        #         while max_n > 1:
        #             data = Data(3,self.n,f.read(512))