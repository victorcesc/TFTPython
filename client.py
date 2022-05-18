# importando as bibliotecas
# ClientTFTP onde está a implementação do protocolo
# e sys para mandar o comando exit()
from ClientTFTP import ClientTFTP
import sys

try:
    # verifica se tem o prmeiro argumento da linha de comando
    # e armazena em IP
    IP = sys.argv[1]
except:
    # senão avisa como deveria ser passado o comando
    # e finaliza o programa, assim se repete para os outros try except
    print('Uso: %s endereco_IP porta timeout nome_do_arquivo ' % sys.argv[0])
    sys.exit()
try:
    # verifica se tem o segundo argumento da linha de comando,
    # converte para inteiro e armazena em PORT
    PORT = int(sys.argv[2])
except:
    print('Uso: %s endereco_IP porta timeout nome_do_arquivo ' % sys.argv[0])
    sys.exit()
try:
    # verifica se tem o terceiro argumento da linha de comando,
    # converte para inteiro e armazena em TIMEOUT
    TIMEOUT = int(sys.argv[3])
except:
    print('Uso: %s endereco_IP porta timeout nome_do_arquivo ' % sys.argv[0])
    sys.exit()
try:
    # verifica se tem o quarto argumento da linha de comando
    # e armazena em NOME_ARQUIVO
    NOME_ARQUIVO = sys.argv[4]
except:
    print('Uso: %s endereco_IP porta timeout nome_do_arquivo ' % sys.argv[0])
    sys.exit()

# modo de transferência TFTP
# foi definido como padrão o netascii
MODE = "netascii"

# cria uma instância do cliente TFTP
# com o ip e porta do servidor e o timeout como argumentos
cliente = ClientTFTP(IP, PORT, TIMEOUT)

# chama a função recebe do cliente TFTP
# que envia solicitação para o servidor
# para que possa baixar o arquivo com o nome passado em linha de comando
cliente.recebe(NOME_ARQUIVO, MODE)
