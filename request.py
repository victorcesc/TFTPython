from message import Message


#opcode 1 = RRQ
#opcode 2 = WRQ
class Request(Message):
    def __init__(self,opcode,filename,mode):
        super().__init__(opcode)
        self.filename = filename
        self.mode = mode
        
    def serialize(self):
        serial = bytearray()
        serial.append(0)        
        serial.append(self.opcode)
        serial += self.filename.encode('ascii')
        serial.append(0)
        serial += self.mode.encode('ascii')
        serial.append(0)
        return serial
       
        
    #se for request preciso fazer algo