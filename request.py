from message import Message


#opcode 1 = RRQ
#opcode 2 = WRQ
class Request(Message):
    def __init__(self,opcode,buffer,filename,mode):
        super().__init__(opcode,buffer)
        if(isinstance(filename, str) & isinstance(mode,str)):
            self.filename = filename.encode('ascii')
            if mode.lower() == "netascii" :
                #traduzir os dados para netascii
                self.mode = mode.encode('ascii')
        else:
            print("filename e mode precisam ser string!!")
        
        
        

       
        
    #se for request preciso fazer algo