class Message:

    #buffer ja vem em bytes e eu preciso traduzir
    #b'0000 0000 0000 0001' - opcode 1
    def __init__(self,opcode,buffer):
        if(isinstance(opcode,int)):            
            self.opcode = opcode            
        else:
            print("esperado um int de opcode")        
        
        self.buffer = buffer
            
        #opcode sempre os 16bits     
        #se for request data ou ack

    def serialize(self):  
        serial = bytearray() 
        serial = self.opcode
        serial += self.buffer
        return serial     
