import sys
from tftp_client.message import Message



class Data(Message):
    def __init__(self,opcode,block,data):
        super().__init__(opcode)
        self.block = block
        self.data = data

#serializa os dados do objeto   
    def serialize(self):
        serial = bytearray()
        serial.append(0)
        serial.append(self.opcode)        
        serial += self.block
        serial += self.data
        return serial