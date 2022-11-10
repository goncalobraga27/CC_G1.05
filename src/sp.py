from re import T
import socket
from sys import argv
from datetime import datetime
import sys
import time
from parserConfFile import parseConfigFile
from parserDataFile import parseDataFile
from answerQuery import aQuery
import threading 
from processQuery import pQuery

class sp:

    def __init__(self, ipSP, domainServer, nameConfig_File, portaUDP, portaTCP_SP, portaTCP_SS, dictDataBase):
        self.ipSP = ipSP
        self.domainServer = domainServer
        self.nameConfig_File = nameConfig_File
        self.portaUDP = portaUDP
        self.portaTCP_SP = portaTCP_SP
        self.portaTCP_SS = portaTCP_SS
        self.dictDataBase = dictDataBase
        self.tamanhoDataBase=0
        self.versao_DataBase=-1
        self.verifTime_DataBase=0
        self.passoZT=0
        self.listaIP_SS=[]
        self.lista_logFile=[]
        self.lockZT=threading.Lock()

    def verificaDomain(d):
        if d==sp.self.domainServer: 
            return True
        else: return False
    def verificaipSS(ip):
        for it in sp.self.listaIP_SS:
            if it==ip: return True
        return False 
    def zoneTransfer(self):
        self.lockZT.acquire()
        sck_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
        sck_TCP.bind((self.ipSP,self.portaTCP_SP))
        sck_TCP.listen()
        connect,add_TCP = sck_TCP.accept()
        msg_TCP = connect.recv(1024)
        msg = msg_TCP
        if msg==" " and self.passoZT==0:
            resposta=str(self.versao_DataBase)+ " "+str(self.verifTime_DataBase)
            connect.send(resposta)
            connect.close()
            self.passoZT+=1
        if msg!=" " and self.passoZT==1:
            if sp.verificaDomain(msg)== True and sp.verificaipSS(add_TCP[0])==True:
                connect.send(self.tamanhoDataBase)
                connect.close()
                self.passoZT+=1
            else:
                self.passoZT=0
        if msg!=" " and self.passoZT==2:
            if int(msg)==self.tamanhoDataBase:
                connect.send(self.dictDataBase)
                connect.close()
            else:
                self.passoZT=0

        self.lockZT.release()
    
    def thread1(self):
        while True:
            th2=threading.Thread(target=self.zoneTransfer)  
            time.sleep(self.verifTime_DataBase)
            th2.start()
            return

    

        
    def runSP(self):
        # O path do ficheiro de dados do SP está armazenado na variável path_FileDataBase
        # A lista com nome listaIP_SS tem armazenado os ips do SS para este SP          Exemplo:  IP-[10.0.1.10,10.0.2.10]
        #                                                                                              |             |
        # A lista com nome listaPorta_SS tem armazenado as portas do SS para este SP           Porta-[3333     ,   3333]
        # A lista com nome listaLogFile tem os paths dos logs files do domain e de todos os dominios (all), basicamente é uma lista com prioridades
        # Exemplo : [Files/logfileSP.txt,Files/logfiles.txt]
        #          Log file do dominio do SP, Log file do all

        parseConfFile = parseConfigFile(self.nameConfig_File)
        listaIP_SS,listaPorta_SS,listaLogFile,pathFileDataBase = parseConfFile.parsingConfigFile()  
        self.listaIP_SS=listaIP_SS
        self.lista_logFile=listaLogFile
        parseDFile = parseDataFile(self.dictDataBase, pathFileDataBase[:-1])
        versao,tempoVerificacao,tamanhoDataBase=parseDFile.parsingDataFile()
        self.versao_DataBase=versao
        self.VerifTime_DataBase=tempoVerificacao
        self.tamanhoDataBase=tamanhoDataBase
        

        sck_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        
        sck_UDP.bind((self.ipSP, self.portaUDP))

        print(f"Estou à escuta no {self.ipSP}:{self.portaUDP}\n")

        while True:
            thZT=threading.Thread(target=self.thread1)              # Onde ocorre a zone transfer 
            thZT.start()

            msg_UDP,add_UDP = sck_UDP.recvfrom(1024)

            print(msg_UDP.decode('utf-8'))

            proQuery_UDP = pQuery(msg_UDP.decode('utf-8'), self.domainServer)

            queryCheck_UDP=proQuery_UDP.processQuery(0)

            if (queryCheck_UDP==False):
                print("A query pedida não é válida")

            else:
                print(f"Recebi uma mensagem do cliente {add_UDP}")
                f=open(self.lista_logFile[0],"a")  
                now = datetime.today().isoformat()
                lineLogFile="{"+str(now)+"} "+"{QR/QE}"+" {"+self.ipSP+":"+str(self.portaUDP)+"} "+ "{"+msg_UDP.decode('utf-8')+"}\n"
                f.write(lineLogFile)
                f.close()
                ansQuery = aQuery(proQuery_UDP.message_id,"R+A",str(0),self.dictDataBase,proQuery_UDP.typeValue)
                resposta = ansQuery.answerQuery()
                respostaDatagram = '\n'.join(resposta)
                b =respostaDatagram.encode('UTF-8')
                sck_UDP.sendto(b,add_UDP)

        sck_UDP.close()

def main():
    ipSP = '10.2.2.2'
    nameConfig_File = argv[1]  # ../Files/ConfigFileSP.txt 
    domainServer = argv[2]
    portaUDP = 3333
    portaTCP_SP = 4444
    portaTCP_SS = 6666
    dictDataBase = dict()
    spObj = sp(ipSP,domainServer,nameConfig_File,portaUDP,portaTCP_SP, portaTCP_SS, dictDataBase)
    spObj.runSP()    

if __name__ == "__main__":
    main()