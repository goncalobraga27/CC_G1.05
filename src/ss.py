import socket
import threading
import time
from datetime import datetime
from random import randint
from sys import argv

from answerQuery import aQuery
from parserConfFile import parseConfigFile
from processQuery import pQuery
from logFile import logF
class controlaDB:
    def __init__(self,versao_DataBase,verifTime_DataBase):
        self.versao=versao_DataBase
        self.verifTime_DataBase=verifTime_DataBase
class ss:
    global dictDataBase
    dictDataBase=dict()
    global Lock 
    Lock=threading.Lock()

    def __init__(self, ipSS, ipSP, domain, nameConfig_File, portaUDP, portaTCP_SP, portaTCP_SS):
        self.nameConfig_File = nameConfig_File
        self.domainServer = domain
        self.ipSS = ipSS
        self.ipSP = ipSP
        self.portaUDP = portaUDP
        self.portaTCP_SP = portaTCP_SP
        self.portaTCP_SS = portaTCP_SS
        self.lista_logFile=[]

    def runsecThread(controlDB,ipSP,portaTCP_SP,domainServer,lista_LogFile):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ipSP,portaTCP_SP))
        Lock.acquire()
        print("Vou enviar a primeira mensagem da ZT")
        msg="ZT"
        s.sendall(msg.encode('utf-8'))
        print("Vou receber a versão da base de dados do sp")
        fstResp=s.recv(1024)
        resp=fstResp.decode('utf-8')
        print(f"A versão da base de dados do sp é esta {resp}")
        print(f"A versão da minha base de dados(ss) é esta {controlDB.versao}")
        if int(resp)!=controlDB.versao:
            controlDB.versao=int(resp)
            print(f"Vou enviar o domínio a que eu pertenço\nO meu domínio é este {domainServer}")
            msg=domainServer
            s.sendall(msg.encode('utf-8'))
            print("Vou receber o número de linhas que foram alteradas na base de dados")
            scdResp=s.recv(1024)
            resp=scdResp.decode('utf-8')
            print("Vou enviar novamente o número de linhas que foram alteradas na base de dados")
            s.sendall(resp.encode('utf-8'))
            print("Vou receber as linhas da base de dados que foram alteradas")
            trdResp=s.recv(1024)
            resp=trdResp.decode('utf-8')
            print(f"As linhas novas que pertencem á base de dados são: {resp}")
            dictDataBase["MX"]=resp         #ATENÇÃO QUE ISTO NÃO PODE ESTAR ASSIM 
            print(dictDataBase)
            print(f"Número da nova versão da base de dados {controlDB.versao}")
            now = datetime.today().isoformat()
            writeLogFile=logF(str(now),"ZT",ipSP+":"+str(portaTCP_SP),"SS",lista_LogFile[0])
            writeLogFile.escritaLogFile()
        else:
            now = datetime.today().isoformat()
            writeLogFile=logF(str(now),"ZT",ipSP+":"+str(portaTCP_SP),"SS",lista_LogFile[0])
            writeLogFile.escritaLogFile()
        Lock.release()

        
    def runfstThread(ipSP,portaTCP_SP,domainServer,listaLogFile,controlDB):
        while True:
            threading.Thread(target=ss.runsecThread,args=(controlDB,ipSP,portaTCP_SP,domainServer,listaLogFile)).start()
            print(f"A versão da data base entre threads é de{controlDB.versao}")
            time.sleep(5) # aqui tem de ser o tempo do soarefresh
        s.close()

    def runSS(self):
        parseConfFile = parseConfigFile(self.nameConfig_File)
        listaIP_SP,listaPorta_SP,listaLogFile,path_FileDataBase=parseConfFile.parsingConfigFile()  
        self.lista_logFile=listaLogFile 
        self.listaIP_SP=listaIP_SP
        if self.listaIP_SP==[] and self.lista_logFile==[] and listaPorta_SP==[]:
            now = datetime.today().isoformat()
            writeLogFile=logF(str(now),"FL","127.0.0.1","Parse config File error",self.lista_logFile[0])
            writeLogFile.escritaLogFile()
        now = datetime.today().isoformat()
        writeLogFile=logF(str(now),"EV","@",self.nameConfig_File+" "+self.lista_logFile[0],self.lista_logFile[0])
        writeLogFile.escritaLogFile()
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
        controlDB=controlaDB(int(-1),int(5))
        threading.Thread(target=ss.runfstThread,args=(self.ipSP,self.portaTCP_SP,self.domainServer,self.lista_logFile,controlDB)).start()

        while True:
            print(dictDataBase)
            msg_UDP,add = sck.recvfrom(1024)

            print(msg_UDP.decode('utf-8'))

            proQuery_UDP = pQuery(msg_UDP.decode('utf-8'), self.domainServer)

            queryCheck_UDP= proQuery_UDP.processQuery(0)

            if(queryCheck_UDP==False):
                print("A query pedida não é válida")
            else:
                print(f"Recebi uma mensagem do cliente {add}")
                now = datetime.today().isoformat()
                writeLogFile=logF(str(now),"QR/QE",self.ipSS+":"+str(self.portaUDP),msg_UDP.decode('utf-8'),self.lista_logFile[0])
                writeLogFile.escritaLogFile()
                ansQuery = aQuery(proQuery_UDP.message_id,"R",str(0),ss.dictDataBase,proQuery_UDP.typeValue)
                resposta = ansQuery.answerQuery()
                respostaDatagram = '\n'.join(resposta)
                b =respostaDatagram.encode('UTF-8')
                sck.sendto(b,add)
                now = datetime.today().isoformat()
                writeLogFile=logF(str(now),"RP/RR",self.ipSS+":"+str(self.portaUDP),respostaDatagram,self.lista_logFile[0])
                writeLogFile.escritaLogFile()

        sck.close()


def main():
    ipSS = '10.4.4.2'
    ipSP = '10.2.2.2'
    nameConfig_File = argv[1]  # ../Files/ConfigFileSS.txt 
    domainServer = argv[2]
    portaUDP = 3333
    portaTCP_SS = 6666
    portaTCP_SP = 4444
    ssObj = ss(ipSS, ipSP, domainServer,nameConfig_File,portaUDP,portaTCP_SP,portaTCP_SS)
    ssObj.runSS()  

if __name__ == '__main__':
    main()
