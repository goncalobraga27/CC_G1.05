import socket
import sys
import threading
import time
from datetime import datetime
from re import T
from answerQuery import aQuery
from parserConfigFileST import parseConfigFileST
from processQuery import pQuery


class st:
    def __init__(self,ipST,nameConfig_File):
        self.ipST=ipST
        self.nameConfig_File=nameConfig_File
        self.mainDomain=""
        self.ipSDT=""
        self.portaSDT=""

    def runThreadST(ipST,ipSDT,portaSDT):
        lock=threading.Lock()
        lock.acquire()
        sck =socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        sck.bind((ipST,3332))
        while True:
            msg,add = sck.recvfrom(1024)
            resposta=ipSDT+":"+portaSDT
            sck.sendto(resposta.encode('UTF-8'),add)
        lock.release()
        
    def runST(self):
        parseConfigFile = parseConfigFileST(self.nameConfig_File)
        mainDomain,ipSDT,portaSDT=parseConfigFile.parsingConfigFile()
        self.mainDomain=mainDomain
        self.ipSDT=ipSDT
        self.portaSDT=portaSDT
        threading.Thread(target=st.runThreadST, args=(self.ipST,self.ipSDT,self.portaSDT)).start()



def main():
    ipST = sys.argv[1]    # Porta:3332
    nameConfig_File = sys.argv[2]  # ../Files/ConfigFileST.txt 
    stObj = st(ipST,nameConfig_File)
    stObj.runST()    

if __name__ == "__main__":
    main()