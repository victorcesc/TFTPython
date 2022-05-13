from ClientTFTP import ClientTFTP

IP = '127.0.0.1'
PORT = 5005
TIMEOUT = 10
NOME_ARQUIVO = "host"
MODE = "netascii"

cliente = ClientTFTP(IP, PORT, TIMEOUT)

cliente.envia(NOME_ARQUIVO, MODE)

data = cliente.recv()

print(type(data))

print("resposta do servidor: %s" % data)