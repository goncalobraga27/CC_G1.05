# Started in: 4/12/2022
# Changed by: Gonçalo Braga, João Gonçalves and Miguel Senra
# Finished in: 2/1/23


import datetime
import socket
import sys
from cacheSR import cache
from entryCache import entry
from logFile import logF
from parserConfigFileSR import parseConfigFileSR
class sr:

    def __init__(self,ipSR,portaSR,nameConfigFile):
        self.ipSR=ipSR
        self.portaSR=portaSR
        self.nameConfigFile=nameConfigFile
        self.listaIP_SP=[]
        self.listaIP_SS=[]
        self.listaPorta_SP=[]
        self.listaPorta_SS=[]
        self.listaLogFile=[]
    
    def runSR(self):
        c=cache()
        """
        Parte do parsing do config file do SR
        """
        parseConfigFile = parseConfigFileSR(self.nameConfigFile)
        listaIP_SS,listaPorta_SS,listaIP_SP,listaPorta_SP,listaLogFile=parseConfigFile.parsingConfigFile()
        self.listaIP_SP=listaIP_SP
        self.listaIP_SS=listaIP_SS
        self.listaPorta_SP=listaPorta_SP
        self.listaPorta_SS=listaPorta_SS
        self.listaLogFile=listaLogFile

        if self.listaIP_SP==[] and self.listaIP_SS==[] and self.listaPorta_SP==[] and self.listaPorta_SS==[] and self.listaLogFile==[]:
            now = datetime.today().isoformat()
            writeLogFile=logF(str(now),"FL","127.0.0.1","Parse config File error",self.listaLogFile[0])
            writeLogFile.escritaLogFile()
        
        """
        Parte da criação de um socket para receber ligações
        """
        sck_UDP =socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        sck_UDP.bind((self.ipSR, self.portaSR))

        sys.stdout.write(f"Estou à escuta no {self.ipSR}:{self.portaSR}\n")
        while True:

            e1=entry("campeoesUM.lei","MX","mx1.campeoesUM.lei","15","10","SP","5s","0","Valid")
            e2=entry("campeoesUM.lei","MX","mx2.campeoesUM.lei","17","10","SP","5s","0","Valid")
            e3=entry("campeoesUM.lei","MX","mx3.campeoesUM.lei","18","10","SP","2s","0","Valid")
            e4=entry("campeoesUM.lei","MX","mx4.campeoesUM.lei","18","10","SP","1s","0","Valid")
            c.addEntry(e1)
            c.addEntry(e2)
            c.addEntry(e3)
            c.addEntry(e4)





        


def main():
    ipSR=sys.argv[1]
    nameConfigFile = sys.argv[2]
    srObj=sr(ipSR,3333,nameConfigFile)
    srObj.runSR()

if __name__ == "__main__":
    main()