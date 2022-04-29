import socket

class ClientTFTP:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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