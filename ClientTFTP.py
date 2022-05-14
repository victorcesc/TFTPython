from socket import *
import struct
import sys
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

    def envia(self, nomearq:str, mode:str):
        msg = Request(1,nomearq,mode)  #RRQ
        self.mode = mode 
        self.datafile = nomearq
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

    def handle_rx0(self,msg,timeout:bool=False):
         # n = bloco         
        self.n = 1                
        msg_size = sys.getsizeof( msg )
        print(msg_size)
        print("recebido do server %s" % msg)
        # self.max_n = 1 + self.msg_size/512
        if msg_size < 512:             
            block_n = struct.pack(">H",self.n)
            ack = Ack(4,block_n)
            self._sock.sendto(ack.serialize(),(self.ip,self.port)) 
            self.n = self.n + 1                 
            self._state_handler = self.handle_rx2
        elif msg_size >= 512:
            block_n = struct.pack(">H",self.n)
            ack = Ack(4,block_n)
            self._sock.sendto(ack.serialize(),(self.ip,self.port))
            self.n = self.n + 1
            self._state_handler = self.handle_rx1       
        else:
            self._state_handler = self.handle_timeout


    def handle_rx1(self,msg,timeout:bool=False):
        msg_size = sys.getsizeof( msg )
        if msg_size >= 512:
            block_n = struct.pack(">H",self.n)
            ack = Ack(4,block_n)            
            self._sock.sendto(ack.serialize(),(self.ip,self.port))
            self.n = self.n + 1
        else:
            self._state_handler = self.handle_rx2 #proximo estado

    def handle_rx2(self,msg,timeout:bool=False):
       # timer = 0
       # if msg = Data      
        msg_size = sys.getsizeof( msg ) 
        if msg_size < 512:             
            block_n = struct.pack(">H",self.n)
            ack = Ack(4,block_n)
            self._sock.sendto(ack.serialize(),(self.ip,self.port))
            self._state_handler = self.handle_timeout
            #fecha o arquivo
            self.file.close()
        

    def handle(self):
        # logica do cliente tftp maquina de estados e etc
        # recebe mensagem do socket
        data, addr = self._sock.recvfrom(512)
        # escrevendo no arquivo
        self.file.write(data)
        self._state_handler(data)
        
    def handle_timeout(self): 
        self.disable_timeout()
        self.disable()       
        self._state_handler(None,True)
