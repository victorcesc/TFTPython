from socket import *
import struct
import sys
from ack import Ack
from request import Request
from data import Data
from pypoller import poller #import pode estar errado


class ClientTFTP(poller.Callback):

    def __init__(self, ip:str, port:int , tout:float):
        self.server = ip
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
        self._sock.sendto(msg.serialize(),(self.server,self.port))        
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
        self.msg_size = sys.getsizeof( msg )
        # self.max_n = 1 + self.msg_size/512
        if self.msg_size < 512: 
            
            self.n = struct.pack(">H",0)
            ack = Ack(4,self.n)
            self._sock.sendto(ack.serialize(),(self.server,self.port))         
            self._state_handler = self.handle_rx2
        else:
            self._state_handler = self.handle_rx1         
        

         #proximo estado

    def handle_rx1(self,msg,timeout:bool=False):

        



        self._state_handler = self.handle_rx2 #proximo estado

    def handle_rx2(self,msg,timeout:bool=False):
       # timer = 0
       # if msg = Data
       self.n = struct.pack(">H",0)
       ack = Ack(4,self.n)

    def handle(self):
        # logica do cliente tftp maquina de estados e etc
        # recebe mensagem do socket
        data, addr = self._sock.recvfrom(512)
        self._state_handler(data)
        
    def handle_timeout(self):
        self._state_handler(None,True)

    def recv(self):
        try:
            data, addr = self.client.recvfrom(512)
        except Exception as e:
            print('Erro ao receber')

        return data

        # if arq.length < 512:
        #     return "TERMINATE" 
        # else:
        #     print("Recebidos : %s " % (dados.encode()))
        #     return "ACK"

#     @staticmethod
#     def cria_com_buffer(buffer):
#         # faz algo
#         return Teste(...)
    
#     @staticmethod
#     def cria_com_args(buffer):
#         # faz algo
#         return Teste(...)

# obj = Teste.cria_com_buffer(...)