from socket import *
from request import Request
from .pypoller import poller #import pode estar errado


class ClientTFTP(poller.Callback):

    def __init__(self,ip:str, port:int , tout:float):
        self.server = ip
        self.port = port        
        self._sock = socket(AF_INET, SOCK_DGRAM)
        poller.Callback.__init__(self,self._sock, tout)
        self._state_handler = None
        
        

    def envia(self, nomearq:str, mode:str):
        msg = Request(2,nomearq,mode)
        self._sock.sendto(msg.serialize(),(self.server,self.port))

        self.enable()
        self.enable_timeout()

        sched = poller.Poller()

        #maquina de estados
        self._state_handler = self.handle_tx0
        sched.adiciona(self)
        sched.despache()


    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def handle_tx0(self,msg,timeout:bool=False):
        #msg = msg recebida do handler do poller q foi enviada pelo server
        #N=1
        #MAX_N = 1+LEN/512
        #recebe uma mensagem tipo ?ACK_0 / !DATA_N
        #verifico se a mensagem foi do tipo ACK_0(tipo ack bloco 0) que vem apos o WRQ se for passa para o proximo estado
        

        self._state_handler = self.handle_tx1 #proximo estado

    def handle_tx1(self,msg,timeout:bool=False):
        #enquanto ?ACK_N && N<MAX_N-1 / N++,!DATA_N
        #aqui mantem ate um timeout ou uma mensagem (?ACK_N && N == MAX_N-1)/N++,!DATA_N

        self._state_handler = self.handle_tx2 #proximo estado

    def handle_tx2(self,msg,timeout:bool=False):
        #TIMEOUT / !DATA_N FICA TENTANDO ENVIAR ATE RECEBER UM ACK, CASO CONTRARIO TIMEOUT
        pass

    def handle(self):
        #logica do cliente tftp maquina de estados e etc
        # recebe mensagem do socket
        data, addr = self._sock.recvfrom(512)
        self._state_handler(data)
        

    def handle_timeout(self):
        self._state_handler(None,True)
        

    

    def send(self, bytes):                
        try:
            self.client.sendto(bytes, (self.ip, self.port))
        except Exception as e:
            print('Erro ao enviar')

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