class Message:

    # inicializando a classe mensagem
    def __init__(self,buffer):
        if type(buffer) != int:
            self.opcode = buffer[:2]
            self.buffer = buffer
            #logica pra verificar qual tipo de mensagem
        else:
            self.opcode = buffer
            # opcode sempre os 16bits     
            # se for request data ou ack

    # obtem o opcode da mensagem
    def getOpcode(self):
        return self.opcode

    # serializa os dados do objeto
    def serialize(self):  
        serial = bytearray()
        serial += self.buffer
        return serial     
