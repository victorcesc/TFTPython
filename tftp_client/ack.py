from tftp_client.message import Message

# inicio da classe ack herdando da classe mensagem
class Ack(Message):
    def __init__(self,opcode,block):
        super().__init__(opcode)
        self.block = block

    # serializa os dados do objeto
    def serialize(self):
        serial = bytearray()
        serial.append(0)
        serial.append(self.opcode)        
        serial += self.block
        return serial