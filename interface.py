from socket import *


class TftpHandler:



def __init__(self,ip,port):
    self.port = port
    self.ip = ip
    

def sendBlock(self,bytes):
    # tem q ser servidor
    bloco = bytes
    try:
        #self.cliente.sendto(bloco.encode(),(this.ip,this.port))
    except Exception as e:
        print('Erro ao enviar')

def receive(self):

    try:
        #dados,addr = self.cliente.recvfrom(512)
    except Exception as e:
    if dados < 512 bytes:
        return "TERMINATE" 
    else:
        print("Recebidos : %s " % (dados.encode()))
        return "ACK"




