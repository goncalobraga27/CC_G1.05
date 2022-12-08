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
from processQuery import pQuery
from logFile import logF
from answerQuerySR import aQuerySR

from re import T
from processQuery import pQuery
from logFile import logF


class sr:

    def __init__(self,ipSR,portaSR,nameConfigFile,domainSR):
        self.ipSR=ipSR
        self.portaSR=portaSR
        self.nameConfigFile=nameConfigFile
        self.domainSR=domainSR
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

            msg_UDP,add_UDP = sck_UDP.recvfrom(1024)

            sys.stdout.write(msg_UDP.decode('utf-8'))
            proQuery_UDP = pQuery(msg_UDP.decode('utf-8'), self.domainSR)
            queryCheck_UDP=proQuery_UDP.processQuery(0)

            if (queryCheck_UDP==False):
                sys.stdout.write("\nA query pedida não é válida\n")
            else:
                """
                Parte onde se pede os dados a um servidor(NESTE CASO AINDA SÓ PEDE AO SP!!!!!!!!!!!!!!)
                """
                sys.stdout.write(f"\nRecebi uma mensagem do cliente {add_UDP}\n")
                now = datetime.today().isoformat()
                writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),msg_UDP.decode('utf-8'),self.listaLogFile[0])
                writeLogFile.escritaLogFile()
                sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                pedido=proQuery_UDP.typeValue.encode('UTF-8')
                print(f"PEDIDO FEITO NO SR {pedido}")
                sck.sendto(pedido, (self.listaIP_SP[0], 3332))
                msg_UDP,add_UDP_SR = sck.recvfrom(1024)
                numberLinhas=int(msg_UDP.decode('UTF-8'))

                for i in range(0,numberLinhas):
                    msg_UDP,add_UDP_SR = sck.recvfrom(1024)
                    linha=msg_UDP.decode('UTF-8')
                    listaParametrosLinha=linha.split(' ')
                    e1=entry(self.domainSR,proQuery_UDP.typeValue,listaParametrosLinha[2],listaParametrosLinha[3],listaParametrosLinha[4],"SP","0","0","Valid")
                    c.addEntry(e1)
                
                ansQuerySR = aQuerySR(proQuery_UDP.message_id,"R",str(0),c.cache,proQuery_UDP.typeValue)
                resposta = ansQuerySR.answerQuerySR()
                respostaDatagram = '\n'.join(resposta)
                b =respostaDatagram.encode('UTF-8')
                sck_UDP.sendto(b,add_UDP)




        


def main():
    ipSR=sys.argv[1]
    nameConfigFile = sys.argv[2]
    domainSR=sys.argv[3]
    srObj=sr(ipSR,3333,nameConfigFile,domainSR)
    srObj.runSR()

if __name__ == "__main__":
    main()