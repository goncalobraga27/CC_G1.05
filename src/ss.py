from datetime import datetime
import socket
from sys import argv
import threading
import time
from processQuery import pQuery
from parserConfFile import parseConfigFile
from answerQuery import aQuery
from random import randint

class ss:

    def __init__(self, ipSS, ipSP, domain, nameConfig_File, portaUDP, portaTCP_SP, portaTCP_SS, dictDataBase):
        self.nameConfig_File = nameConfig_File
        self.domainServer = domain
        self.ipSS = ipSS
        self.ipSP = ipSP
        self.portaUDP = portaUDP
        self.portaTCP_SP = portaTCP_SP
        self.portaTCP_SS = portaTCP_SS
        self.dictDataBase = dictDataBase
        self.lista_logFile=[]
        self.versao_DataBase=-1
        self.verifTime_DataBase=0

    
    def enviarFstMsg(socket):
        msg=""
        socket.sendall(msg.encode('utf-8'))

    def receberFstResp(socket):
        fstResp=socket.recv(1024)
        resp=fstResp.decode('utf-8')
        return int(resp)
    
    def enviarScdMsg(self,socket):
        msg=self.domainServer
        socket.sendall(msg.encode('utf-8'))
    
    def receberScdResp(socket):
        scdResp=socket.recv(1024)
        resp=scdResp.decode('utf-8')
        return int(resp)
    
    def enviarTrdMsg(socket,valor):
        msg=str(valor)
        socket.sendall(msg.encode('utf-8'))

    def receberTrdResp(self,socket):
        trdResp=socket.recv(1024)
        resp=trdResp.decode('utf-8')
        self.dictDataBase=resp
        
   
    def runsecThread(self):
        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.connect((self.ipSP,self.portaTCP_SP))
        ss.enviarFstMsg(socket)
        resp= ss.receberFstResp(socket)
        if self.versao_DataBase!=resp:
            ss.enviarScdMsg(socket)
            resp= ss.receberScdResp(socket)
            ss.enviarTrdMsg(socket,resp)
            ss.receberTrdResp(socket)

        
    def runfstThread(self):
        while True:
            threading.Thread(target=ss.runsecThread,arg=(self)).start()
            time.sleep(5) # aqui tem de ser o tempo do soarefresh
        s.close()

    def runSS(self):
        parseConfFile = parseConfigFile(self.nameConfig_File)
        listaIP_SP,listaPorta_SP,listaLogFile,path_FileDataBase=parseConfFile.parsingConfigFile()  
        self.lista_logFile=listaLogFile 
        # O path do ficheiro de dados do SS está armazenado na variável path_FileDataBase
        # A lista com nome listaIP_SP tem armazenado o ips do SP para este SS         Exemplo:  IP-[10.0.1.10]
        #                                                                                              |   
        # A lista com nome listaPorta_SP tem armazenado as portas do SP para este SS         Porta-[3333]
        # A lista com nome listaLogFile tem os paths dos logs files do domain e de todos os dominios (all), basicamente é uma lista com prioridades
        # Exemplo : [Files/logfileSS.txt,Files/logfiles.txt]
        #          Log file do dominio do SS, Log file do all
        
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sck.bind((self.ipSS, self.portaUDP))

        print(f"Estou à escuta no {self.ipSS}:{self.portaUDP}")

        #threading.Thread(target=ss.runfstThread,arg=()).start()

        while True:

            msg_UDP,add = sck.recvfrom(1024)

            print(msg_UDP.decode('utf-8'))

            proQuery_UDP = pQuery(msg_UDP.decode('utf-8'), self.domainServer)

            queryCheck_UDP= proQuery_UDP.processQuery(0)

            if(queryCheck_UDP==False):
                print("A query pedida não é válida")
            else:
                print(f"Recebi uma mensagem do cliente {add}")
                f=open(self.lista_logFile[0],"a")  
                now = datetime.today().isoformat()
                lineLogFile="{"+str(now)+"} "+"{QR/QE}"+" {"+self.ipSS+":"+str(self.portaUDP)+"} "+ "{"+msg_UDP.decode('utf-8')+"}\n"
                f.write(lineLogFile)
                f.close()
                ansQuery = aQuery(proQuery_UDP.message_id,"R",str(0),self.dictDataBase,proQuery_UDP.typeValue)
                resposta = ansQuery.answerQuery()
                respostaDatagram = '\n'.join(resposta)
                b =respostaDatagram.encode('UTF-8')
                sck.sendto(b,add)

        sck.close()


def main():
    ipSS = '10.4.4.2'
    ipSP = '10.2.2.2'
    nameConfig_File = argv[1]  # ../Files/ConfigFileSS.txt 
    domainServer = argv[2]
    portaUDP = 3333
    portaTCP_SS = 6666
    portaTCP_SP = 4444
    dictDataBase = {}
    ssObj = ss(ipSS, ipSP, domainServer,nameConfig_File,portaUDP,portaTCP_SP,portaTCP_SS, dictDataBase)
    ssObj.runSS()  

if __name__ == '__main__':
    main()
