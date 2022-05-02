class Message:

   
    def __init__(self,buffer):
        #teste pra ver se vai ser criado por bytes ou nao
        if type(buffer) != int:
            self.opcode = buffer[:2]
            self.buffer = buffer
            #logica pra verificar qual tipo de mensagem
        else:
            self.opcode = buffer
            
        #opcode sempre os 16bits     
        #se for request data ou ack

    def getOpcode(self):
        return self.opcode

    def serialize(self):  
        serial = bytearray()
        serial += self.buffer
        return serial     
