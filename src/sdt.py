import socket
import sys
import threading
import time
from datetime import datetime
from re import T
from parserConfigFileSDT import parseConfigFileSDT


class sdt:
    def __init__(self,ipSDT,nameConfig_File):
        self.ipSDT=ipSDT
        self.nameConfig_File=nameConfig_File
        self.dictionary=dict()

    def runThreadSDT(ipSDT,dic):
        lock=threading.Lock()
        lock.acquire()
        sck =socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        sck.bind((ipSDT,3334))
        while True:
            msg,add = sck.recvfrom(1024)
            resposta=dic[msg.decode('UTF-8')]
            sck.sendto(resposta.encode('UTF-8'),add)
        lock.release()
        
    def runSDT(self):
        parseConfigFile = parseConfigFileSDT(self.nameConfig_File)
        dic=parseConfigFile.parsingConfigFile()
        self.dictionary=dic
        threading.Thread(target=sdt.runThreadSDT, args=(self.ipSDT,self.dictionary)).start()



def main():
    ipSDT = sys.argv[1]    # Porta:3334
    nameConfig_File = sys.argv[2]  # ../Files/ConfigFileSDT.txt 
    stObj = sdt(ipSDT,nameConfig_File)
    stObj.runSDT()    

if __name__ == "__main__":
    main()