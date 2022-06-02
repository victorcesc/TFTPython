import os
from socket import *
import struct
from ack import Ack
from request import Request
from data import Data
from pypoller import poller #import pode estar errado


class ClientTFTP(poller.Callback):

    def __init__(self, ip:str, port:int , tout:float):
        self.ip = ip
        self.port = port        
        self._sock = socket(AF_INET, SOCK_DGRAM)
        poller.Callback.__init__(self,self._sock, tout)
        self._state_handler = None
        self.n = 0
        self.max_n = 0
        self.msg_size = 0
        self.mode = None
        self.datafile = None

    def recebe(self,nomearq:str, mode:str):
        msg = Request(1,nomearq,mode)  #RRQ
        self.mode = mode 
        self.datafile = nomearq
        self.n = 1
        # cria o arquivo para escrita de bytes
        self.file = open("./"+self.datafile, "wb")  
        self._sock.sendto(msg.serialize(),(self.ip,self.port))        
        self.enable()
        self.enable_timeout()
        sched = poller.Poller()
        #maquina de estados
        self._state_handler = self.handle_rx0
        sched.adiciona(self)
        sched.despache()

    def envia(self,nomearq:str,mode:str):
        msg = Request(2,nomearq,mode) #WRQ
        self.mode = mode 
        self.datafile = nomearq
        self.n = 1
        # cria o arquivo para escrita de bytes
        self.file = open("./"+self.datafile, "rb")
        # size = os.path.getsize(self.file)
        size = os.path.getsize("./"+self.datafile)
        print(size)
        self.max_n = 1 + size/512 
        self._sock.sendto(msg.serialize(),(self.ip,self.port))        
        self.enable()
        self.enable_timeout()
        sched = poller.Poller()
        #maquina de estados
        self._state_handler = self.handle_tx0
        sched.adiciona(self)
        sched.despache()

    def handle_rx0(self,msg,timeout:bool=False):
         # n = bloco         
        msg_size = len( msg ) - 4
        if msg_size < 512:                      
            self._state_handler = self.handle_rx2
        elif msg_size == 512:           
            self._state_handler = self.handle_rx1
        

    def handle_rx1(self,msg,timeout:bool=False):        
        msg_size = len( msg ) - 4
        data_m = int.from_bytes(msg[2:4],"big")
        if msg_size == 512:
            block_n = struct.pack(">H",self.n)
            ack = Ack(4,block_n)            
            self._sock.sendto(ack.serialize(),(self.ip,self.port))
            self.n = self.n + 1
        elif data_m != self.n:
            block_n = struct.pack(">H",data_m)
            ack = Ack(4,block_n)
            self._sock.sendto(ack.serialize(),(self.ip,self.port))
        else:
            self._state_handler = self.handle_rx2 #proximo estado

    def handle_rx2(self,msg,timeout:bool=False):     
        if(msg == None):  
            self.file.close()           
        else:   
            msg_size = len( msg )
            if msg_size < 512:
                block_n = struct.pack(">H",self.n)
                ack = Ack(4,block_n)
                self._sock.sendto(ack.serialize(),(self.ip,self.port))
                self.file.close()
                
                  
    def handle_tx0(self,msg,timeout:bool = False):
        # msg = ack
        ack_n = msg[2:4]
        ack_n = int.from_bytes(ack_n)
        if ack_n == 0:
            dados = self.file.read(512)
            block_n = struct.pack(">H",self.n)
            data_t = Data(3,block_n,dados)
            self._sock.sendto(data_t.serialize(),(self.ip,self.port))
            self._state_handler = self.handle_tx1
       
        
        
    def handle_tx1(self,msg,timeout:bool = False):
        ack_n = msg[2:4]
        ack_n = int.from_bytes(ack_n)
        # if ack_n and self.n < (self.max_n - 1):
        if ack_n == self.n and self.n < (self.max_n - 1):
            self.n = self.n + 1
            dados = self.file.read(512)
            block_n = struct.pack(">H",self.n)
            data_t = Data(3,block_n,dados)
            self._sock.sendto(data_t.serialize(),(self.ip,self.port))
        elif ack_n and (self.n == (self.max_n - 1)):
            self._state_handler = self.handle_tx2

        
    def handle_tx2(self,msg,timeout:bool = False):
        if msg != None:
            self.n = self.n + 1
            dados = self.file.read(512)
            block_n = struct.pack(">H",self.n)
            data_t = Data(3,block_n,dados)
            self._sock.sendto(data_t.serialize(),(self.ip,self.port))
        


    def handle(self):
        # logica do cliente tftp maquina de estados e etc
        # recebe mensagem do socket
        data, addr = self._sock.recvfrom(516) #512 + opcode e blockN     
        # escrevendo no arquivo
        
        opcode = data[0:2]
        opcode = int.from_bytes(opcode, "big") 
       
        if opcode == 1: #WRQ 
            self._state_handler = self.handle_tx0
        if opcode == 2: #RRQ             
            self._state_handler = self.handle_rx0
        if opcode == 3:
            msg = data[4:516]                   
            if msg != None:           
                self.file.write(msg)          
                self._state_handler = self.handle_rx0
                   
        
    def handle_timeout(self): 
        self.disable_timeout()
        self.disable()       
        self._state_handler = self.handle_timeout
