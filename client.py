import * from TftpHandler

ip = '127.0.0.1'
port = '69'

cliente = TftpHandler(ip,port)

TftpHandler.sendBlock('nomedoarq.teste' , b'12312412\n')

#no tftp preciso saber o arquivo la no 
# servidor para poder recebe-lo no client

dados = TftpHandler.receive('nomedoarquivo.exemplo')
