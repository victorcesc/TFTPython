from ClientTFTP import ClientTFTP

IP = '127.0.0.1'
PORT = 5005
TIMEOUT = 5
NOME_ARQUIVO = "host"
MODE = "netascii"

cliente = ClientTFTP(IP, PORT, TIMEOUT)

cliente.envia(NOME_ARQUIVO, MODE)

#cliente.handle()

