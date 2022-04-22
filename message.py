class Message:

    #buffer ja vem em bytes e eu preciso traduzir
    #b'0000 0000 0000 0001' - opcode 1
    def __init__(self,opcode,buffer):
        self.opcode = opcode
        self.buffer = buffer
        self.opcode = int.from_bytes(opcode)
        print(self.opcode)
        #opcode sempre os 16bits     
        #se for request data ou ack

        

