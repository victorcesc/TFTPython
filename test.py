# importando as bibliotecas
# ClientTFTP onde está a implementação do protocolo
# e sys para mandar o comando exit()
from tftp_client import client_tftp
import sys

try:
    # verifica se tem o prmeiro argumento da linha de comando
    # e armazena em IP
    IP = sys.argv[1]
except:
    # senão avisa como deveria ser passado o comando
    # e finaliza o programa, assim se repete para os outros try except
    print('Uso: %s endereco_IP porta timeout nome_do_arquivo modo_envio(1-RRQ 2-WRQ)' % sys.argv[0])
    sys.exit()
try:
    # verifica se tem o segundo argumento da linha de comando,
    # converte para inteiro e armazena em PORT
    PORT = int(sys.argv[2])
except:
    print('Uso: %s endereco_IP porta timeout nome_do_arquivo modo_envio(1-RRQ 2-WRQ)' % sys.argv[0])
    sys.exit()
try:
    # verifica se tem o terceiro argumento da linha de comando,
    # converte para inteiro e armazena em TIMEOUT
    TIMEOUT = int(sys.argv[3])
except:
    print('Uso: %s endereco_IP porta timeout nome_do_arquivo modo_envio(1-RRQ 2-WRQ)' % sys.argv[0])
    sys.exit()
try:
    # verifica se tem o quarto argumento da linha de comando
    # e armazena em NOME_ARQUIVO
    NOME_ARQUIVO = sys.argv[4]
except:
    print('Uso: %s endereco_IP porta timeout nome_do_arquivo modo_envio(1-RRQ 2-WRQ)' % sys.argv[0])
    sys.exit()
try:
    # Modo servidor(envia ou recebe) ou cliente tftp 1 para enviar uma RRQ ou 2 para WRQ
    MODO = int(sys.argv[5])
except:
    print('Uso: %s endereco_IP porta timeout nome_do_arquivo modo_envio(1-RRQ 2-WRQ)' % sys.argv[0])
    sys.exit()

# modo de transferência TFTP
# foi definido como padrão o netascii
MODE = "NetAscii"

# cria uma instância do cliente TFTP
# com o ip e porta do servidor e o timeout como argumentos
cliente = client_tftp.ClientTFTP(IP, PORT, TIMEOUT)

# chama a função recebe do cliente TFTP
# que envia solicitação para o servidor
# para que possa baixar o arquivo com o nome passado em linha de comando
if MODO == 1:
    cliente.recebe(NOME_ARQUIVO,MODE)
if MODO == 2:
    cliente.envia(NOME_ARQUIVO,MODE)
