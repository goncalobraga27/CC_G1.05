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
from messageDNS import MessageDNS

class hd:
    
    def __init__(self,proQuery,add_UDP,domain,c,sck_UDP,msg_UDP,listaIP_ST,listaPorta_ST,ipSR,portaSR,listaLogFile,listaIP_SP):
        self.proQuery = proQuery
        self.add_UDP = add_UDP
        self.domain = domain
        self.c = c
        self.sck_UDP = sck_UDP
        self.msg_UDP = msg_UDP
        self.listaIP_ST=listaIP_ST
        self.listaPorta_ST=listaPorta_ST
        self.ipSR=ipSR
        self.portaSR=portaSR
        self.listaLogFile=listaLogFile
        self.listaIP_SP=listaIP_SP
        

    def perguntaAoSeuSP(self):
        """
        Parte onde se pede os dados ao servidor primário do domínio 
        """
        sys.stdout.write(f"\nRecebi uma mensagem do cliente {self.add_UDP}\n")
        now = datetime.now()
        writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),self.msg_UDP,self.listaLogFile[0])
        writeLogFile.escritaLogFile()
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pedido=self.proQuery.typeValue.encode('UTF-8')
        sck.sendto(pedido, (self.listaIP_SP[0], 3332))
        msg_UDP,add_UDP_SR = sck.recvfrom(1024)
        
        numberLinhas=int(msg_UDP.decode('UTF-8'))
        for i in range(0,numberLinhas+1):
            msg_UDP,add_UDP_SR = sck.recvfrom(1024)
            linha=msg_UDP.decode('UTF-8')
            listaParametrosLinha=linha.split(' ')
            if(len(listaParametrosLinha)==3):
                ttlS=listaParametrosLinha[2]
                ttl=int(ttlS)
            if(len(listaParametrosLinha)==6):
                e1=entry(self.domain,self.proQuery.typeValue,listaParametrosLinha[3],ttl,listaParametrosLinha[5],"SP",datetime.now(),"0","VALID")  
                self.c.addEntry(e1)
            if(len(listaParametrosLinha)==5):
                e1=entry(self.domain,self.proQuery.typeValue,listaParametrosLinha[3],ttl,"0","SP",datetime.now(),"0","VALID")
                self.c.addEntry(e1)
        
        ansQuerySR = aQuerySR(self.proQuery.message_id,"R",str(2),self.c.cache,self.proQuery.typeValue,self.domain)
        resposta,cod_message = ansQuerySR.answerQuerySR()
        respostaDatagram = '\n'.join(resposta)
        self.sck_UDP.sendto(cod_message,self.add_UDP)
    
    def perguntaLEIandSRLEI(self):
        query="Give the address of .lei SDT".encode('UTF-8')
        sckST = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sckST.sendto(query,(self.listaIP_ST[0],int(self.listaPorta_ST[0])))
        msg,add = sckST.recvfrom(1024)
        listaParSDT=msg.decode('UTF-8').split(':')
        now = datetime.now()
        writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),"PEDIDO DE INFORMAÇÃO AO SDT",self.listaLogFile[0])
        writeLogFile.escritaLogFile()
        sckSDT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sckSDT.sendto(self.domain.encode('UTF-8'),(listaParSDT[0],int(listaParSDT[1])))
        msg,add = sckSDT.recvfrom(1024)
        now = datetime.now()
        writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),"PEDIDO DE INFORMAÇÃO AO SP",self.listaLogFile[0])
        writeLogFile.escritaLogFile()
        listaIP=msg.decode('UTF-8').split(':')
        sckSP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pedido = self.proQuery.typeValue.encode('UTF-8')
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
                e1=entry(self.domain,self.proQuery.typeValue,listaParametrosLinha[3],ttl,listaParametrosLinha[5],"SP",datetime.now(),"0","VALID")  
                self.c.addEntry(e1)
            if(len(listaParametrosLinha)==5):
                e1=entry(self.domain,self.proQuery.typeValue,listaParametrosLinha[3],ttl,0,"SP",datetime.now(),"0","VALID")
                self.c.addEntry(e1)
        ansQuerySR = aQuerySR(self.proQuery.message_id,"R",str(2),self.c.cache,self.proQuery.typeValue,self.domain)
        resposta,cod_message = ansQuerySR.answerQuerySR()
        respostaDatagram = '\n'.join(resposta)
        b =respostaDatagram.encode('UTF-8')
        now = datetime.now()
        writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),respostaDatagram,self.listaLogFile[0])
        writeLogFile.escritaLogFile()
        self.sck_UDP.sendto(b,self.add_UDP)
    
    def perguntaLEIandSRMEI(self):
        query="Give the address of .mei SDT".encode('UTF-8')
        sckST = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sckST.sendto(query,(self.listaIP_ST[1],int(self.listaPorta_ST[1])))
        msg,add = sckST.recvfrom(1024)
        now = datetime.now()
        writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),"PEDIDO DE INFORMAÇÃO AO SDT",self.listaLogFile[0])
        writeLogFile.escritaLogFile()
        listaParSDT=msg.decode('UTF-8').split(':')
        sckSDT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sckSDT.sendto(self.domain.encode('UTF-8'),(listaParSDT[0],int(listaParSDT[1])))
        msg,add = sckSDT.recvfrom(1024)
        now = datetime.now()
        writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),"PEDIDO DE INFORMAÇÃO AO SP",self.listaLogFile[0])
        writeLogFile.escritaLogFile()
        listaIP=msg.decode('UTF-8').split(':')
        sckSP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pedido = self.proQuery.typeValue.encode('UTF-8')
        sckSP.sendto(pedido, (listaIP[0], int(listaIP[1])))
        msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
        numberLinhas=int(msg_UDP.decode('UTF-8'))

        for i in range(0,numberLinhas+1):
            msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
            linha=msg_UDP.decode('UTF-8')
            print(linha)
            listaParametrosLinha=linha.split(' ')
            if(len(listaParametrosLinha)==3):
                ttlS=listaParametrosLinha[2]
                ttl=int(ttlS)
            if(len(listaParametrosLinha)==6):
                e1=entry(self.domain,self.proQuery.typeValue,listaParametrosLinha[3],ttl,listaParametrosLinha[5],"SP",datetime.now(),"0","VALID")  
                self.c.addEntry(e1)
            if(len(listaParametrosLinha)==5):
                e1=entry(self.domain,self.proQuery.typeValue,listaParametrosLinha[3],ttl,0,"SP",datetime.now(),"0","VALID")
                self.c.addEntry(e1)
        
        ansQuerySR = aQuerySR(self.proQuery.message_id,"R",str(2),self.c.cache,self.proQuery.typeValue,self.domain)
        resposta,cod_message = ansQuerySR.answerQuerySR()
        respostaDatagram = '\n'.join(resposta)
        b =respostaDatagram.encode('UTF-8')
        now = datetime.now()
        writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),respostaDatagram,self.listaLogFile[0])
        writeLogFile.escritaLogFile()
        self.sck_UDP.sendto(b,self.add_UDP)


    def perguntaMEIandSRLEI(self):
        query="Give the address of .lei SDT".encode('UTF-8')
        sckST = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sckST.sendto(query,(self.listaIP_ST[1],int(self.listaPorta_ST[1])))
        msg,add = sckST.recvfrom(1024)
        now = datetime.now()
        writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),"PEDIDO DE INFORMAÇÃO AO SDT",self.listaLogFile[0])
        writeLogFile.escritaLogFile()
        listaParSDT=msg.decode('UTF-8').split(':')
        sckSDT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(self.domain)
        sckSDT.sendto(self.domain.encode('UTF-8'),(listaParSDT[0],int(listaParSDT[1])))
        msg,add = sckSDT.recvfrom(1024)
        now = datetime.now()
        writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),"PEDIDO DE INFORMAÇÃO AO SP",self.listaLogFile[0])
        writeLogFile.escritaLogFile()
        listaIP=msg.decode('UTF-8').split(':')
        sckSP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pedido = self.proQuery.typeValue.encode('UTF-8')
        sckSP.sendto(pedido, (listaIP[0], int(listaIP[1])))
        msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
        numberLinhas=int(msg_UDP.decode('UTF-8'))

        for i in range(0,numberLinhas+1):
            msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
            linha=msg_UDP.decode('UTF-8')
            listaParametrosLinha=linha.split(' ')
            if(len(listaParametrosLinha)==3):
                ttlS=listaParametrosLinha[2]
                ttl=int(ttlS)
            if(len(listaParametrosLinha)==6):
                e1=entry(self.domain,self.proQuery.typeValue,listaParametrosLinha[3],ttl,listaParametrosLinha[5],"SP",datetime.now(),"0","VALID")  
                self.c.addEntry(e1)
            if(len(listaParametrosLinha)==5):
                e1=entry(self.domain,self.proQuery.typeValue,listaParametrosLinha[3],ttl,0,"SP",datetime.now(),"0","VALID")
                self.c.addEntry(e1)
        
        ansQuerySR = aQuerySR(self.proQuery.message_id,"R",str(2),self.c.cache,self.proQuery.typeValue,self.domain)
        resposta,cod_message = ansQuerySR.answerQuerySR()
        respostaDatagram = '\n'.join(resposta)
        b =respostaDatagram.encode('UTF-8')
        now = datetime.now()
        writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),respostaDatagram,self.listaLogFile[0])
        writeLogFile.escritaLogFile()
        self.sck_UDP.sendto(b,self.add_UDP)

    
    def perguntaMEIandSRMEI(self):
        query="Give the address of .mei SDT".encode('UTF-8')
        sckST = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sckST.sendto(query,(self.listaIP_ST[0],int(self.listaPorta_ST[0])))
        msg,add = sckST.recvfrom(1024)
        now = datetime.now()
        writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),"PEDIDO DE INFORMAÇÃO AO SDT",self.listaLogFile[0])
        writeLogFile.escritaLogFile()
        listaParSDT=msg.decode('UTF-8').split(':')
        sckSDT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sckSDT.sendto(self.domain.encode('UTF-8'),(listaParSDT[0],int(listaParSDT[1])))
        msg,add = sckSDT.recvfrom(1024)
        now = datetime.now()
        writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),"PEDIDO DE INFORMAÇÃO AO SP",self.listaLogFile[0])
        writeLogFile.escritaLogFile()
        listaIP=msg.decode('UTF-8').split(':')
        sckSP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pedido = self.proQuery.typeValue.encode('UTF-8')
        sckSP.sendto(pedido, (listaIP[0], int(listaIP[1])))
        msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
        numberLinhas=int(msg_UDP.decode('UTF-8'))

        for i in range(0,numberLinhas+1):
            msg_UDP,add_UDP_SR = sckSP.recvfrom(1024)
            linha=msg_UDP.decode('UTF-8')
            print(linha)
            "campeoesUC.mei @ MX mx1.campeoesUC.mei TTL 11"
            listaParametrosLinha=linha.split(' ')
            if(len(listaParametrosLinha)==3):
                ttlS=listaParametrosLinha[2]
                ttl=int(ttlS)
            if(len(listaParametrosLinha)==6):
                e1=entry(self.domain,self.proQuery.typeValue,listaParametrosLinha[3],ttl,listaParametrosLinha[5],"SP",datetime.now(),"0","VALID")  
                self.c.addEntry(e1)
            if(len(listaParametrosLinha)==5):
                e1=entry(self.domain,self.proQuery.typeValue,listaParametrosLinha[3],ttl,0,"SP",datetime.now(),"0","VALID")
                self.c.addEntry(e1)
    
        ansQuerySR = aQuerySR(self.proQuery.message_id,"R",str(2),self.c.cache,self.proQuery.typeValue,self.domain)
        resposta,cod_message = ansQuerySR.answerQuerySR()
        respostaDatagram = '\n'.join(resposta)
        b =respostaDatagram.encode('UTF-8')
        now = datetime.now()
        writeLogFile=logF(str(now),"QR/QE",self.ipSR+":"+str(self.portaSR),respostaDatagram,self.listaLogFile[0])
        writeLogFile.escritaLogFile()
        self.sck_UDP.sendto(cod_message,self.add_UDP)
