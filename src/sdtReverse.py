import socket
import sys
import threading
import time
from datetime import datetime
from re import T
from parserConfigFileST import parseConfigFileST


class sdtReverse:
    def __init__(self,ipSDTreverse,nameConfig_File):
        self.ipSDTreverse=ipSDTreverse
        self.nameConfig_File=nameConfig_File
        self.mainDomain=""
        self.ipSPreverse=""
        self.portaSPreverse=""

    def runThreadSDT(ipSDT,ipSP,portaSP):
        lock=threading.Lock()
        lock.acquire()
        sck =socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        sck.bind((ipSDT,3332))
        while True:
            msg,add = sck.recvfrom(1024)
            print("Recebi pedido")
            resposta="O servidor com este endereçamento é que te pode ajudar "+ipSP+":"+portaSP
            sck.sendto(resposta.encode('UTF-8'),add)
        lock.release()
        
    def runSDT(self):
        parseConfigFile = parseConfigFileST(self.nameConfig_File)
        mainDomain,ipSPreverse,portaSPreverse=parseConfigFile.parsingConfigFile()
        self.mainDomain=mainDomain
        self.ipSPreverse=ipSPreverse
        self.portaSPreverse=portaSPreverse
        threading.Thread(target=sdtReverse.runThreadSDT, args=(self.ipSDTreverse,self.ipSPreverse,self.portaSPreverse)).start()



def main():
    ipSDTreverse = sys.argv[1]  
    nameConfig_File = sys.argv[2]  
    stObj = sdtReverse(ipSDTreverse,nameConfig_File)
    stObj.runSDT()    

if __name__ == "__main__":
    main()