from socket import *


class TftpHandler:


    def __init__(self,ip,port):
        self.port = port
        self.ip = ip
        cliente = socket(AF_INET, SOCK_DGRAM,17)
        cliente.bind(('0.0.0.0',5555))


    def sendBlock(self,bytes):
        bloco = bytes
        
        try:
            self.cliente.sendto(bloco.encode(),(self.ip,self.port))
        except Exception as e:
            print('Erro ao enviar')

    def receive(self,arq,arqlocal):
        try:
            dados,addr = self.cliente.recvfrom(512)
        except Exception as e:
        if dados < 512 bytes:
            return "TERMINATE" 
        else:
            print("Recebidos : %s " % (dados.encode()))
            return "ACK"




