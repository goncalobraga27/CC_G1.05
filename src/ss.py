# Started in: 31/09/2022
# Changed by: Gonçalo Braga, João Gonçalves and Miguel Senra
# Finished in: 23/11/2022
import socket
import sys
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
    """
    Classe que serve para controlo dos dados que surgem da zone transfer, tal como a versão da base de dados que possui 
    e do tempo de verificação dos dados da base de dados(espécie do TTL da base de dados)
    """
    def __init__(self,versao_DataBase,verifTime_DataBase):
        self.versao=versao_DataBase
        self.verifTime_DataBase=verifTime_DataBase

class ss:
    global dictDataBase               # Variável global que vai servir para armazenar os dados recebidos na ZT
    dictDataBase=dict()               # Inicialização da variável global 
    global Lock                       # Variável global que garante controlo de concorrência na zt
    Lock=threading.Lock()             # Inicialização da variável global 

    def __init__(self, ipSS, ipSP, domain, nameConfig_File, portaUDP, portaTCP_SP, portaTCP_SS,modo):
        """
        Criação/Inicialização da classe ss
        """
        self.nameConfig_File = nameConfig_File
        self.domainServer = domain
        self.ipSS = ipSS
        self.ipSP = ipSP
        self.portaUDP = portaUDP
        self.portaTCP_SP = portaTCP_SP
        self.portaTCP_SS = portaTCP_SS
        self.lista_logFile=[]
        self.debug=modo
    
    def iniciaBaseDados(dicDataBase):
        """
        Inicialização da base de dados para poder receber os dados que são provenientes da ZT
        """
        dicDataBase["DEFAULT"]=[]
        dicDataBase["SOASP"]=[]
        dicDataBase["SOAADMIN"]=[]
        dicDataBase["SOASERIAL"]=[]
        dicDataBase["SOAREFRESH"]=[]
        dicDataBase["SOARETRY"]=[]
        dicDataBase["SOAEXPIRE"]=[]
        dicDataBase["NS"]=[]
        dicDataBase["A"]=[]
        dicDataBase["CNAME"]=[]
        dicDataBase["MX"]=[]
        dicDataBase["PTR"]=[]

    def addBaseDados(dictDataBase,resp,flag):
        """
        Acrescenta uma linha recebida, proveniente da zt á base de dados do SP
        """
        linhaP=resp.split('-')
        if len(linhaP)!=1:
            conteudo=linhaP[1]
            if int(linhaP[0])!=flag: return False
            linhaPContent=conteudo.split(' ')
            dictDataBase[linhaPContent[1]].append(conteudo)
        return True 

    def runsecThread(self,controlDB):
        """
        Esta função é a função que realmente realiza trabalho na zone transfer, tal como enviar queries ao SP a pedir dados da base de dados e o seu processamento.
        Como podemos visualizar, é criado um protocolo para a zone transfer entre servidores.
        A especificação do protocolo aqui estabelecido, encontra-se devidamente ilustrado no relatório da primeira fase do trabalho.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ipSP,self.portaTCP_SP))
        Lock.acquire()
        if self.debug==1:
            sys.stdout.write("Vou enviar a primeira mensagem da ZT\n")
        msg="ZT"
        s.sendall(msg.encode('utf-8'))
        if self.debug==1:    
            sys.stdout.write("Vou receber a versão da base de dados do sp\n")
        fstResp=s.recv(1024)
        resp=fstResp.decode('utf-8')
        versaoandTTLDB=resp.split(' ')
        versaoDB=int(versaoandTTLDB[0])
        controlDB.verifTime_DataBase=int(versaoandTTLDB[1])
        if self.debug==1:
            sys.stdout.write(f"A versão da base de dados do sp é esta {versaoDB}\n")
            sys.stdout.write(f"A versão da minha base de dados(ss) é esta {controlDB.versao}\n")
        if versaoDB!=controlDB.versao:
            if self.debug==1:
                sys.stdout.write(f"Vou enviar o domínio a que eu pertenço\nO meu domínio é este {self.domainServer}\n")
            msg=self.domainServer
            s.sendall(msg.encode('utf-8'))
            if self.debug==1:
                sys.stdout.write("Vou receber o número de linhas que foram alteradas na base de dados\n")
            scdResp=s.recv(1024)
            resp=scdResp.decode('utf-8')
            if self.debug==1:    
                sys.stdout.write("Vou enviar novamente o número de linhas que foram alteradas na base de dados\n")
            s.sendall(resp.encode('utf-8'))
            if self.debug==1:
                sys.stdout.write("Vou receber as linhas da base de dados que foram alteradas\n")
            ss.iniciaBaseDados(dictDataBase)
            flag=1
            verification=True
            for i in range(int(resp)-1):
                if verification==True:
                    tamanhoLinha=int(s.recv(2).decode('utf-8'))
                    trdResp=s.recv(tamanhoLinha)
                    resp=trdResp.decode('utf-8')
                    verification=ss.addBaseDados(dictDataBase,resp,flag)
                    if not verification:
                        if self.debug==1:
                            sys.stdout.write("A transmissão da base de dados deu problemas\n")
                        s.close()
                    flag+=1
            controlDB.versao=versaoDB
            if self.debug==1:
                sys.stdout.write(f"Número da nova versão da base de dados {controlDB.versao}\n")
            now = datetime.today().isoformat()
            writeLogFile=logF(str(now),"ZT",self.ipSP+":"+str(self.portaTCP_SP),"SS",self.lista_logFile[0])
            writeLogFile.escritaLogFile()
        else:
            now = datetime.today().isoformat()
            writeLogFile=logF(str(now),"ZT",self.ipSP+":"+str(self.portaTCP_SP),"SS",self.lista_logFile[0])
            writeLogFile.escritaLogFile()
        Lock.release()

    def runfstThread(self,controlDB):
        """
        Esta função serve de controlo da ZT
        A metodologia utilizada na mesma é a seguinte:
        Como sabemos que é o ss que decide o timing de pedir os dados ao sp podemos fazer o seguinte
        1º Criar um ciclo, para a ZT ser realizada enquanto que o servidor estiver ativo 
        2º Chamar múltiplas threads para realizar a ZT
        3º Fazer a ZT em intervalos de verifTime_DataBase segundos a zone transfer 
        """
        while True:
            threading.Thread(target=ss.runsecThread,args=(self,controlDB)).start()
            if self.debug==1:
                sys.stdout.write(f"A versão da data base entre threads é de{controlDB.versao}\n")
            time.sleep(controlDB.verifTime_DataBase) 
        s.close()

    def runSS(self):
        """
        O path do ficheiro de dados do SS está armazenado na variável path_FileDataBase
        A lista com nome listaIP_SP tem armazenado o ips do SP para este SS         Exemplo:  IP-[10.0.1.10]
                                                                                                      |   
        A lista com nome listaPorta_SP tem armazenado as portas do SP para este SS         Porta-[3333]
        A lista com nome listaLogFile tem os paths dos logs files do domain e de todos os dominios (all), basicamente é uma lista com prioridades
        Exemplo : [Files/logfileSS.txt,Files/logfiles.txt]
                  Log file do dominio do SS, Log file do all

        A metodologia utilizada nesta função é a seguinte:
        1º Parsing dos ficheiros necessários para o arranque do componente
        2º É inicializado os processos de transferência de zona entre o servidor primário 
        3º O servidor secundário, depois de obter os dados da base de dados do seu sp, encontra-se disponível para responder a queries do cliente 
        que lhe sejam pedidas 

        DISCLAIMER: Depois de feita a inicialização de todos os processos que ocorrem no SS, este encontra disponível para realizar este processos ciclicamente
        """

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
    
        
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sck.bind((self.ipSS, self.portaUDP))

        if self.debug==1:    
            sys.stdout.write(f"Estou à escuta no {self.ipSS}:{self.portaUDP}\n")
        controlDB=controlaDB(int(-1),int(5))
        threading.Thread(target=ss.runfstThread,args=(self,controlDB,)).start()
        while True:
            msg_UDP,add = sck.recvfrom(1024)

            if self.debug==1:
                sys.stdout.write(msg_UDP.decode('utf-8'))

            proQuery_UDP = pQuery(msg_UDP.decode('utf-8'), self.domainServer)

            queryCheck_UDP= proQuery_UDP.processQuery(0)

            if(queryCheck_UDP==False):
                if self.debug==1:
                    sys.stdout.write("\nA query pedida não é válida\n")
            else:
                if self.debug==1:    
                    sys.stdout.write(f"\nRecebi uma mensagem do cliente {add}\n")
                now = datetime.today().isoformat()
                writeLogFile=logF(str(now),"QR/QE",self.ipSS+":"+str(self.portaUDP),msg_UDP.decode('utf-8'),self.lista_logFile[0])
                writeLogFile.escritaLogFile()
                ansQuery= aQuery(proQuery_UDP.message_id,"R",str(0),dictDataBase,proQuery_UDP.typeValue)
                resposta= ansQuery.answerQuery()
                respostaDatagram = '\n'.join(resposta)
                b =respostaDatagram.encode('UTF-8')
                sck.sendto(b,add)
                now = datetime.today().isoformat()
                writeLogFile=logF(str(now),"RP/RR",self.ipSS+":"+str(self.portaUDP),respostaDatagram,self.lista_logFile[0])
                writeLogFile.escritaLogFile()

        sck.close()


def main():
    ipSS = sys.argv[1]
    ipSP = sys.argv[2]
    nameConfig_File = sys.argv[3]  # ../Files/ConfigFileSS.txt 
    domainServer = sys.argv[4]
    debug=0
    if len(sys.argv)==6:
        debug=int(sys.argv[5])
    portaUDP = 3333
    portaTCP_SS = 6666
    portaTCP_SP = 4444
    ssObj = ss(ipSS, ipSP, domainServer,nameConfig_File,portaUDP,portaTCP_SP,portaTCP_SS,debug)
    ssObj.runSS()  

if __name__ == '__main__':
    main()
