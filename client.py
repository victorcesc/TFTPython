from ClientTFTP import ClientTFTP

IP = '127.0.0.1'
PORT = 5005
MESSAGE = b"Jhonatan"

cliente = ClientTFTP(IP, PORT)

cliente.send(MESSAGE)

data = cliente.recv()
print("resposta do servidor: %s" % data)