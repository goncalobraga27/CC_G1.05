import socket
import sys
import threading
import time
from datetime import datetime
from re import T
from answerQuery import aQuery
from parserConfigFileST import parseConfigFileST
from processQuery import pQuery


class streverse:
    def __init__(self,ipSTreverse,nameConfig_File):
        self.ipSTreverse=ipSTreverse
        self.nameConfig_File=nameConfig_File
        self.mainDomain=""
        self.ipSDTreverse=""
        self.portaSDTreverse=""

    def runThreadST(ipST,ipSDT,portaSDT):
        lock=threading.Lock()
        lock.acquire()
        sck =socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        sck.bind((ipST,3332))
        while True:
            msg,add = sck.recvfrom(1024)
            print("Recebi pedido")
            resposta="O servidor com este endereçamento é que te pode ajudar "+ipSDT+":"+portaSDT
            sck.sendto(resposta.encode('UTF-8'),add)
        lock.release()
        
    def runST(self):
        parseConfigFile = parseConfigFileST(self.nameConfig_File)
        mainDomain,ipSDTreverse,portaSDTreverse=parseConfigFile.parsingConfigFile()
        self.mainDomain=mainDomain
        self.ipSDTreverse=ipSDTreverse
        self.portaSDTreverse=portaSDTreverse
        threading.Thread(target=streverse.runThreadST, args=(self.ipSTreverse,self.ipSDTreverse,self.portaSDTreverse)).start()



def main():
    ipSTreverse = sys.argv[1]    # Porta:3332
    nameConfig_File = sys.argv[2]  # ../Files/ConfigFileSTreverse.txt 
    stObj = streverse(ipSTreverse,nameConfig_File)
    stObj.runST()    

if __name__ == "__main__":
    main()