# Started in: 4/12/2022
# Changed by: Gonçalo Braga, João Gonçalves and Miguel Senra
# Finished in: 2/1/23


from cacheSR import cache
from entryCache import entry
import socket
import sys
import threading
import time
from datetime import datetime
from random import randint
from sys import argv
from parserConfigFileSR import parseConfigFileSR
from processQuerySR import pQuerySR
from logFile import logF
from answerQuerySR import aQuerySR
from threadCache import thrCache
from re import T
from processQuery import pQuery
from logFile import logF
from handler import hd

class sr:

    def __init__(self,ipSR,portaSR,nameConfigFile,domainSR):
        self.ipSR=ipSR
        self.portaSR=portaSR
        self.nameConfigFile=nameConfigFile
        self.domainSR=domainSR
        self.listaIP_SP=[]
        self.listaPorta_SP=[]
        self.listaLogFile=[]
        self.listaIP_ST=[]
        self.listaPorta_ST=[]
    
    def runSR(self):
        c=cache()
        threading.Thread(target=thrCache.runControlCache, args=(c,)).start()
        """
        Parte do parsing do config file do SR
        """
        parseConfigFile = parseConfigFileSR(self.nameConfigFile)
        listaIP_SP,listaPorta_SP,listaLogFile,listaIP_ST,listaPorta_ST=parseConfigFile.parsingConfigFile()
        self.listaIP_SP=listaIP_SP
        self.listaPorta_SP=listaPorta_SP
        self.listaLogFile=listaLogFile
        self.listaIP_ST=listaIP_ST
        self.listaPorta_ST=listaPorta_ST
        if self.listaIP_SP==[] and self.listaPorta_SP==[] and  self.listaLogFile==[]:
            now = datetime.now()
            writeLogFile=logF(str(now),"FL","127.0.0.1","Parse config File error",self.listaLogFile[0])
            writeLogFile.escritaLogFile()
        
        """
        Parte da criação de um socket para receber ligações
        """
        sck_UDP =socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        sck_UDP.bind((self.ipSR, self.portaSR))

        sys.stdout.write(f"Estou à escuta no {self.ipSR}:{self.portaSR}\n")
        while True:

            msg_UDP,add_UDP = sck_UDP.recvfrom(1024)

            sys.stdout.write(msg_UDP.decode('utf-8')+"\n")
            proQuery = pQuerySR(msg_UDP.decode('utf-8'))
            queryCheck,domain=proQuery.processQuery()

            ansQuerySR = aQuerySR(proQuery.message_id,"",str(0),c.cache,proQuery.typeValue,domain)
            if (queryCheck==1):
                sys.stdout.write("\nA query pedida não é válida\n")
            if (queryCheck==0 and ansQuerySR.canGiveResponse()==True):
                resposta = ansQuerySR.answerQuerySR()
                respostaDatagram = '\n'.join(resposta)
                b =respostaDatagram.encode('UTF-8')
                sck_UDP.sendto(b,add_UDP)
            else:
                if (queryCheck==0 and domain==self.domainSR):
                    hd.perguntaAoSeuSP(self,proQuery,add_UDP,domain,c,sck_UDP,msg_UDP)
                if (queryCheck==0 and domain!=self.domainSR):
                    domainQ=domain.split('.')
                    domainsSR=self.domainSR.split('.')
                    if(domainQ[1]=="lei"):
                        if (domainsSR[1]=="lei"):
                            hd.perguntaLEIandSRLEI(self,domain,proQuery,c,sck_UDP,add_UDP)
                        if(domainsSR[1]=="mei"):
                            hd.perguntaLEIandSRMEI(self,domain,proQuery,c,sck_UDP,add_UDP)
                    if(domainQ[1]=="mei"):
                        if (domainsSR[1]=="lei"):
                            hd.perguntaMEIandSRLEI(self,domain,proQuery,c,sck_UDP,add_UDP)
                        if(domainsSR[1]=="mei"):
                            hd.perguntaMEIandSRMEI(self,domain,proQuery,c,add_UDP,sck_UDP)

def main():
    ipSR=sys.argv[1]
    nameConfigFile = sys.argv[2]
    domainSR=sys.argv[3]
    srObj=sr(ipSR,3333,nameConfigFile,domainSR)
    srObj.runSR()

if __name__ == "__main__":
    main()