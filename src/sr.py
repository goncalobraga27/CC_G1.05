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

            ansQuerySR = aQuerySR(proQuery.message_id,"R",str(0),c.cache,proQuery.typeValue,domain)
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
                    """
                    Parte onde se pede os dados ao servidor primário do domínio 
                
                    sys.stdout.write(f"\nRecebi uma mensagem do cliente {add_UDP}\n")
                    now = datetime.now()
                    writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),msg_UDP.decode('utf-8'),self.listaLogFile[0])
                    writeLogFile.escritaLogFile()
                    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    pedido=proQuery.typeValue.encode('UTF-8')
                    sck.sendto(pedido, (self.listaIP_SP[0], 3332))
                    msg_UDP,add_UDP_SR = sck.recvfrom(1024)
                    numberLinhas=int(msg_UDP.decode('UTF-8'))

                    for i in range(0,numberLinhas):
                        msg_UDP,add_UDP_SR = sck.recvfrom(1024)
                        linha=msg_UDP.decode('UTF-8')
                        listaParametrosLinha=linha.split(' ')
                        if(len(listaParametrosLinha)==3):
                            ttlS=listaParametrosLinha[2]
                            ttl=int(ttlS)
                        if(len(listaParametrosLinha)==6):
                            e1=entry(domain,proQuery.typeValue,listaParametrosLinha[3],ttl,listaParametrosLinha[5],"SP",datetime.now(),"0","VALID")  
                            c.addEntry(e1)
                        if(len(listaParametrosLinha)==5):
                            e1=entry(domain,proQuery.typeValue,listaParametrosLinha[3],ttl,"0","SP",datetime.now(),"0","VALID")
                            c.addEntry(e1)

            
                    ansQuerySR = aQuerySR(proQuery.message_id,"R",str(0),c.cache,proQuery.typeValue,domain)
                    resposta = ansQuerySR.answerQuerySR()
                    respostaDatagram = '\n'.join(resposta)
                    b =respostaDatagram.encode('UTF-8')
                    sck_UDP.sendto(b,add_UDP)
                    """
                if (queryCheck==0 and domain!=self.domainSR):
                    domainQ=domain.split('.')
                    domainsSR=self.domainSR.split('.')
                    if(domainQ[1]=="lei"):
                        if (domainsSR[1]=="lei"):
                            hd.perguntaLEIandSRLEI(self,domain,proQuery,c,sck_UDP,add_UDP)
                            """
                            query="Give the address of .lei SDT".encode('UTF-8')
                            sckST = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sckST.sendto(query,(self.listaIP_ST[0],int(self.listaPorta_ST[0])))
                            msg,add = sckST.recvfrom(1024)
                            listaParSDT=msg.decode('UTF-8').split(':')
                            sckSDT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sckSDT.sendto(domain.encode('UTF-8'),(listaParSDT[0],int(listaParSDT[1])))
                            msg,add = sckSDT.recvfrom(1024)
                            listaIP=msg.decode('UTF-8').split(':')
                            sckSP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            pedido=proQuery.typeValue.encode('UTF-8')
                            sckSP.sendto(pedido, (listaIP[0], int(listaIP[1])))
                            msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
                            numberLinhas=int(msg_UDP.decode('UTF-8'))

                            for i in range(0,numberLinhas):
                                msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
                                linha=msg_UDP.decode('UTF-8')
                                print(linha)
                                listaParametrosLinha=linha.split(' ')
                                if(len(listaParametrosLinha)==3):
                                    ttlS=listaParametrosLinha[2]
                                    ttl=int(ttlS)
                                if(len(listaParametrosLinha)==6):
                                    e1=entry(domain,proQuery.typeValue,listaParametrosLinha[3],ttl,listaParametrosLinha[5],"SP",datetime.now(),"0","VALID")  
                                    c.addEntry(e1)
                                if(len(listaParametrosLinha)==5):
                                    e1=entry(domain,proQuery.typeValue,listaParametrosLinha[3],ttl,0,"SP",datetime.now(),"0","VALID")
                                    c.addEntry(e1)
                            
                            ansQuerySR = aQuerySR(proQuery.message_id,"R",str(0),c.cache,proQuery.typeValue,domain)
                            resposta = ansQuerySR.answerQuerySR()
                            respostaDatagram = '\n'.join(resposta)
                            b =respostaDatagram.encode('UTF-8')
                            sck_UDP.sendto(b,add_UDP)
                            """
                        if(domainsSR[1]=="mei"):
                            hd.perguntaLEIandSRMEI(self,domain,proQuery,c,sck_UDP,add_UDP)
                            """
                            query="Give the address of .mei SDT".encode('UTF-8')
                            sckST = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sckST.sendto(query,(self.listaIP_ST[1],int(self.listaPorta_ST[1])))
                            msg,add = sckST.recvfrom(1024)
                            listaParSDT=msg.decode('UTF-8').split(':')
                            sckSDT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sckSDT.sendto(domain.encode('UTF-8'),(listaParSDT[0],int(listaParSDT[1])))
                            msg,add = sckSDT.recvfrom(1024)
                            listaIP=msg.decode('UTF-8').split(':')
                            sckSP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            pedido=proQuery.typeValue.encode('UTF-8')
                            sckSP.sendto(pedido, (listaIP[0], int(listaIP[1])))
                            msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
                            numberLinhas=int(msg_UDP.decode('UTF-8'))

                            for i in range(0,numberLinhas):
                                msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
                                linha=msg_UDP.decode('UTF-8')
                                print(linha)
                                listaParametrosLinha=linha.split(' ')
                                if(len(listaParametrosLinha)==3):
                                    ttlS=listaParametrosLinha[2]
                                    ttl=int(ttlS)
                                if(len(listaParametrosLinha)==6):
                                    e1=entry(domain,proQuery.typeValue,listaParametrosLinha[3],ttl,listaParametrosLinha[5],"SP",datetime.now(),"0","VALID")  
                                    c.addEntry(e1)
                                if(len(listaParametrosLinha)==5):
                                    e1=entry(domain,proQuery.typeValue,listaParametrosLinha[3],ttl,0,"SP",datetime.now(),"0","VALID")
                                    c.addEntry(e1)
                            
                            ansQuerySR = aQuerySR(proQuery.message_id,"R",str(0),c.cache,proQuery.typeValue,domain)
                            resposta = ansQuerySR.answerQuerySR()
                            respostaDatagram = '\n'.join(resposta)
                            b =respostaDatagram.encode('UTF-8')
                            sck_UDP.sendto(b,add_UDP)
                            """
                    if(domainQ[1]=="mei"):
                        if (domainsSR[1]=="lei"):
                            hd.perguntaMEIandSRLEI(self,domain,proQuery,c,sck_UDP,add_UDP)
                            """
                            query="Give the address of .lei SDT".encode('UTF-8')
                            sckST = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sckST.sendto(query,(self.listaIP_ST[1],int(self.listaPorta_ST[1])))
                            msg,add = sckST.recvfrom(1024)
                            listaParSDT=msg.decode('UTF-8').split(':')
                            sckSDT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sckSDT.sendto(domain.encode('UTF-8'),(listaParSDT[0],int(listaParSDT[1])))
                            msg,add = sckSDT.recvfrom(1024)
                            listaIP=msg.decode('UTF-8').split(':')
                            sckSP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            pedido=proQuery.typeValue.encode('UTF-8')
                            sckSP.sendto(pedido, (listaIP[0], int(listaIP[1])))
                            msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
                            numberLinhas=int(msg_UDP.decode('UTF-8'))

                            for i in range(0,numberLinhas):
                                msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
                                linha=msg_UDP.decode('UTF-8')
                                listaParametrosLinha=linha.split(' ')
                                if(len(listaParametrosLinha)==3):
                                    ttlS=listaParametrosLinha[2]
                                    ttl=int(ttlS)
                                if(len(listaParametrosLinha)==6):
                                    e1=entry(domain,proQuery.typeValue,listaParametrosLinha[3],ttl,listaParametrosLinha[5],"SP",datetime.now(),"0","VALID")  
                                    c.addEntry(e1)
                                if(len(listaParametrosLinha)==5):
                                    e1=entry(domain,proQuery.typeValue,listaParametrosLinha[3],ttl,0,"SP",datetime.now(),"0","VALID")
                                    c.addEntry(e1)
                            
                            ansQuerySR = aQuerySR(proQuery.message_id,"R",str(0),c.cache,proQuery.typeValue,domain)
                            resposta = ansQuerySR.answerQuerySR()
                            respostaDatagram = '\n'.join(resposta)
                            b =respostaDatagram.encode('UTF-8')
                            sck_UDP.sendto(b,add_UDP)
                            """
                        if(domainsSR[1]=="mei"):
                            hd.perguntaMEIandSRMEI(self,domain,proQuery,c,add_UDP,sck_UDP)
                            """
                            query="Give the address of .mei SDT".encode('UTF-8')
                            sckST = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sckST.sendto(query,(self.listaIP_ST[0],int(self.listaPorta_ST[0])))
                            msg,add = sckST.recvfrom(1024)
                            listaParSDT=msg.decode('UTF-8').split(':')
                            sckSDT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sckSDT.sendto(domain.encode('UTF-8'),(listaParSDT[0],int(listaParSDT[1])))
                            msg,add = sckSDT.recvfrom(1024)
                            listaIP=msg.decode('UTF-8').split(':')
                            sckSP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            pedido=proQuery.typeValue.encode('UTF-8')
                            sckSP.sendto(pedido, (listaIP[0], int(listaIP[1])))
                            msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
                            numberLinhas=int(msg_UDP.decode('UTF-8'))

                            for i in range(0,numberLinhas):
                                msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
                                linha=msg_UDP.decode('UTF-8')
                                print(linha)
                                "campeoesUC.mei @ MX mx1.campeoesUC.mei TTL 11"
                                listaParametrosLinha=linha.split(' ')
                                if(len(listaParametrosLinha)==3):
                                    ttlS=listaParametrosLinha[2]
                                    ttl=int(ttlS)
                                if(len(listaParametrosLinha)==6):
                                    e1=entry(domain,proQuery.typeValue,listaParametrosLinha[3],ttl,listaParametrosLinha[5],"SP",datetime.now(),"0","VALID")  
                                    c.addEntry(e1)
                                if(len(listaParametrosLinha)==5):
                                    e1=entry(domain,proQuery.typeValue,listaParametrosLinha[3],ttl,0,"SP",datetime.now(),"0","VALID")
                                    c.addEntry(e1)
                                
                            
                            ansQuerySR = aQuerySR(proQuery.message_id,"R",str(0),c.cache,proQuery.typeValue,domain)
                            resposta = ansQuerySR.answerQuerySR()
                            respostaDatagram = '\n'.join(resposta)
                            b =respostaDatagram.encode('UTF-8')
                            sck_UDP.sendto(b,add_UDP)
                            """

def main():
    ipSR=sys.argv[1]
    nameConfigFile = sys.argv[2]
    domainSR=sys.argv[3]
    srObj=sr(ipSR,3333,nameConfigFile,domainSR)
    srObj.runSR()

if __name__ == "__main__":
    main()