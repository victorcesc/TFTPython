import os
from socket import *
import struct
from tftp_client.ack import Ack
from tftp_client.request import Request
from tftp_client.data import Data
from pypoller import poller #import pode estar errado

# inicio da classe herdando o callback da classe poller
class ClientTFTP(poller.Callback):

    # instância da claase clientTFTP com ip, porta e time out como parâmetros
    def __init__(self, ip:str, port:int , tout:float):
        self.ip = ip
        self.port = port
        # cria um socket do tipo udp
        self._sock = socket(AF_INET, SOCK_DGRAM)
        # inicia o callback do poller passando o socket e o time out como parâmetros
        poller.Callback.__init__(self,self._sock, tout)
        # referencia do estado atual, ou seja, nenhum por enquanto
        self._state_handler = None
        # instância das variáveis
        # número de pacotes
        self.n = 0
        # número de pacotes máximo dependendo do tamanho do arquivo
        self.max_n = 0
        # tamanho máximo da mensagem
        self.msg_size = 0
        # modo do envio
        self.mode = None
        # arquivo de dados que vai ser transferido
        self.datafile = None

    # recebe os dados do servidor tftp
    def recebe(self,nomearq:str, mode:str):
        # cria uma mensagem RRQ - read request
        msg = Request(1,nomearq,mode)  #RRQ
        self.mode = mode 
        self.datafile = nomearq
        self.n = 1
        # cria o arquivo para escrita de bytes
        self.file = open("./"+self.datafile, "wb")
        # envia a mensagem RRQ para o servidor
        self._sock.sendto(msg.serialize(),(self.ip,self.port))
        self.enable()
        self.enable_timeout()
        sched = poller.Poller()
        # máquina de estados
        # define o próximo estado como rx0
        self._state_handler = self.handle_rx0
        sched.adiciona(self)
        sched.despache()

    def envia(self,nomearq:str,mode:str):
        # cria uma mensagem WRQ - write request
        msg = Request(2,nomearq,mode) #WRQ
        self.mode = mode 
        self.datafile = nomearq
        self.n = 1
        # cria o arquivo para leitura de bytes
        self.file = open("./"+self.datafile, "rb")
        # size = os.path.getsize(self.file)
        size = os.path.getsize("./"+self.datafile)
        print(size)
        # determina o número máximo de pacotes
        self.max_n = 1 + size/512
        # envia a mensagem RRQ para o servidor
        self._sock.sendto(msg.serialize(),(self.ip,self.port))        
        self.enable()
        self.enable_timeout()
        sched = poller.Poller()
        # máquina de estados
        # define o próximo estado como tx0
        self._state_handler = self.handle_tx0
        sched.adiciona(self)
        sched.despache()

    # estado rx0 da máquina de estado
    def handle_rx0(self,msg,timeout:bool=False):
         # n = bloco
        msg_size = len( msg ) - 4
        # se o tamanho da mensagem é menor que 512 bytes
        if msg_size < 512:
            block_n = struct.pack(">H",self.n)
            # cria uma mensagem ACK
            ack = Ack(4,block_n)
            # envia a mensagem ACK
            self._sock.sendto(ack.serialize(),(self.ip,self.port))
            # define o próximo estado como rx2           
            self._state_handler = self.handle_rx2
        # se o tamannho da mensagem é igual a 512 bytes
        elif msg_size == 512:
            block_n = struct.pack(">H",self.n)
            # cria uma mensagem ACK
            ack = Ack(4,block_n)
            # envia a mensagem ACK
            self._sock.sendto(ack.serialize(),(self.ip,self.port))
            # incrementa n
            self.n = self.n + 1
            # define o próximo estado como rx1
            self._state_handler = self.handle_rx1
        
    # estado rx1 da máquina de estado
    def handle_rx1(self,msg,timeout:bool=False):
        # tamanho da mensagem
        msg_size = len( msg )
        data_m = int.from_bytes(msg[2:4],"big")
        # se o tamanho da mensagem é igual a 512 bytes
        if msg_size == 512:
            block_n = struct.pack(">H",self.n)
            # cria uma mensagem ACK
            ack = Ack(4,block_n)
            # envia a mensagem ACK
            self._sock.sendto(ack.serialize(),(self.ip,self.port))
            # incrementa n
            self.n = self.n + 1
        elif data_m != self.n:
            block_n = struct.pack(">H",data_m)
            # cria uma mensagem ACK
            ack = Ack(4,block_n)
            # envia a mensagem ACK
            self._sock.sendto(ack.serialize(),(self.ip,self.port))
        else:
            block_n = struct.pack(">H",self.n)
            # cria uma mensagem ACK
            ack = Ack(4,block_n)
            # envia uma mensagem ACK
            self._sock.sendto(ack.serialize(),(self.ip,self.port))
            # define o próximo estado como rx2
            self._state_handler = self.handle_rx2

    # estado rx2 da máquina de estado
    def handle_rx2(self,msg,timeout:bool=False):
        # se mensagem está vazia
        if(msg == None):
            # fecha o arquivo de escrita
            self.file.close()
        # senão
        else:
            msg_size = len( msg )
            # se tamanho da mensagem menor que 512 bytes
            if msg_size < 512:
                block_n = struct.pack(">H",self.n)
                # cria uma mensagem ACK
                ack = Ack(4,block_n)
                # envia uma mensagem ACK
                self._sock.sendto(ack.serialize(),(self.ip,self.port))
                # fecha o arquivo de escrita
                self.file.close()

    # estado tx0 da máquina de estado
    def handle_tx0(self,msg,timeout:bool = False):
        # msg = ack
        ack_n = msg[2:4]
        ack_n = int.from_bytes(ack_n)
        # se ack = 0
        if ack_n == 0:
            # lê 512 bytes do arquivo
            dados = self.file.read(512)
            block_n = struct.pack(">H",self.n)
            # cria uma mensagem DATA
            data_t = Data(3,block_n,dados)
            # envia uma mensagem DATA
            self._sock.sendto(data_t.serialize(),(self.ip,self.port))
            # define o próximo estado como tx1
            self._state_handler = self.handle_tx1

    # estado tx1 da máquina de estado        
    def handle_tx1(self,msg,timeout:bool = False):
        ack_n = msg[2:4]
        ack_n = int.from_bytes(ack_n)
        # if ack_n and self.n < (self.max_n - 1):
        # se número do ack = n e n < n máximo - 1
        if ack_n == self.n and (self.n < (self.max_n - 1)):
            # incrementa n
            self.n = self.n + 1
            # lê 512 bytes do arquivo
            dados = self.file.read(512)
            block_n = struct.pack(">H",self.n)
            # cria uma mensagem DATA
            data_t = Data(3,block_n,dados)
            # envia uma mensagem DATA
            self._sock.sendto(data_t.serialize(),(self.ip,self.port))
        # senão, se número do ack e n = n máximo - 1
        elif ack_n and (self.n == (self.max_n - 1)):
            # incrementa n
            self.n = self.n + 1
            # lê 512 bytes do arquivo
            dados = self.file.read(512)
            block_n = struct.pack(">H",self.n)
            # cria uma mensagem DATA
            data_t = Data(3,block_n,dados)
            # envia uma mensagem DATA
            self._sock.sendto(data_t.serialize(),(self.ip,self.port))
            # define o pŕoximo estado como tx2
            self._state_handler = self.handle_tx2

    # estado tx2 da máquina de estado
    def handle_tx2(self,msg,timeout:bool = False):
        # se mensagem não é vazia
        if msg != None:
            # incrementa n
            self.n = self.n + 1
            # lê 512 bytes do arquivo
            dados = self.file.read(512)
            block_n = struct.pack(">H",self.n)
            # cria uma mensagem DATA
            data_t = Data(3,block_n,dados)
            # envia uma mensagem DATA
            self._sock.sendto(data_t.serialize(),(self.ip,self.port))

    def handle(self):
        # logica do cliente tftp maquina de estados e etc
        # recebe mensagem do socket
        data, addr = self._sock.recvfrom(516) #512 + opcode e blockN     
        # escrevendo no arquivo        
        opcode = data[0:2]
        opcode = int.from_bytes(opcode, "big")     
        if opcode == 3:
            msg = data[4:516]                            
            if msg != None:    
                print(msg)       
                self.file.write(msg)   
                self._state_handler(data)       

    # time out        
    def handle_timeout(self): 
        self.disable_timeout()
        self.disable()       
        self._state_handler = self.handle_timeout