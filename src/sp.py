# Started in: 31/09/2022
# Changed by: Gonçalo Braga, João Gonçalves and Miguel Senra
# Finished in: 23/11/2022

import socket
import sys
import threading
import time
from datetime import datetime
from re import T
from answerQuery import aQuery
from parserConfFile import parseConfigFile
from parserDataFile import parseDataFile
from processQuery import pQuery
from logFile import logF
from threadResolver import thrResolver

class sp:
    
    global dictDataBase              # Variável global que serve como estrutura de dados do SP
    dictDataBase=dict()              # Inicialização da estrutura de dados do SP
    global lock                      # Variável global para controlo de concorrência das threads na transferência de zona 
    lock = threading.Lock()          # Inicialização do Lock
    def __init__(self, ipSP, domainServer, nameConfig_File, portaUDP, portaTCP_SP, portaTCP_SS,modo):
        """
        Criação/Inicialização da classe sp
        """
        self.ipSP = ipSP
        self.domainServer = domainServer
        self.nameConfig_File = nameConfig_File
        self.portaUDP = portaUDP
        self.portaTCP_SP = portaTCP_SP
        self.portaTCP_SS = portaTCP_SS
        self.tamanhoDataBase=0
        self.versao_DataBase=-1
        self.verifTime_DataBase=0
        self.listaIP_SS=[]
        self.lista_logFile=[]
        self.debug=modo

    def verificaDomain(d,domainServer):
        """
        Verifica se dois domínios passados como parâmetros são iguais
        """
        if d==domainServer: 
            return True
        else: 
            return False

    def verificaipSS(ip,listaIP_SS): 
        """
        Verifica se um IP existe numa lista de IP's passados como parâmetro
        """
        for it in listaIP_SS:
            if it==ip: return True
        return False 

    def runfstThread(self):
        """
        Esta função pertence á zone transfer
        A metodologia da função é a seguinte:
        1º Criação/Inicialização de um socket TCP para comunicação entre servidores
        2º Ciclo que serve para aceitar a conexão entre servidores e delega a outra thread o trabalho da zone transfer 

        Esta função serve como "centro de controlo" da zone transfer.
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.bind((self.ipSP,self.portaTCP_SP))
        sock.listen()

        while True:
            connection, address = sock.accept()
            threading.Thread(target=sp.runsecThread,args=(self,connection,address)).start() 
        sock.close()

    def runsecThread(self,connection,address):
        """
        Esta função é a função que realmente realiza trabalho na zone transfer, tal como receber queries TCP do SS e enviar respostas ás queries do SS.
        Como podemos visualizar, é criado um protocolo para a zone transfer entre servidores.
        A especificação do protocolo aqui estabelecido, encontra-se devidamente ilustrado no relatório da primeira fase do trabalho.
        """
        if self.debug==1:
            sys.stdout.write("Vou tratar da parte da ZT no SP\n")
            sys.stdout.write("Vou tratar da parte da ZT no SP\n")

        lock.acquire()
        if self.debug==1:
            sys.stdout.write("Vou receber a primeira mensagem\n")
        msgRecebida = connection.recv(1024)
        msg=msgRecebida.decode('utf-8')
        if self.debug==1:
            sys.stdout.write(f"A mensagem que recebi foi {msg}\n")

        if msg=="ZT":
            if self.debug==1:
                sys.stdout.write(f"Vou enviar a versão da minha base de dados\nA minha versão é esta {str(self.versao_DataBase)}\n")
                print(self.verifTime_DataBase)
                sys.stdout.write(f"O TTL da base de dados que vou enviar é este {self.verifTime_DataBase}\n")
            msgEnviar=str(self.versao_DataBase)+" "+str(self.verifTime_DataBase)
            connection.send(msgEnviar.encode('utf-8'))
            if self.debug==1:
                sys.stdout.write("Vou receber o domínio para o qual se pretende fazer a ZT\n")
            msgRecebida = connection.recv(1024)
            msg=msgRecebida.decode('utf-8')
            if self.debug==1:
                sys.stdout.write(f"O domínio que recebi foi este {msg}\n")

            if sp.verificaDomain(msg,self.domainServer)==True and sp.verificaipSS(address[0],self.listaIP_SS)==True:
                nextStep=True

            else: 
                nextStep=False
                now = datetime.today().isoformat()
                writeLogFile=logF(str(now),"EZ",address[0]+":"+str(6666),"SP",self.lista_logFile[0])
                writeLogFile.escritaLogFile()
            if self.debug==1:    
                sys.stdout.write(f"Foram feitas todas as verificações e o resultado das mesmas é {nextStep}\n")

            if nextStep==True:
                if self.debug==1:
                    sys.stdout.write(f"Vou enviar o tamanho da base de dados\n")
                    sys.stdout.write(f"O tamanho da base de dados é este {self.tamanhoDataBase}\n")
                msgEnviar=str(self.tamanhoDataBase)
                connection.send(msgEnviar.encode('utf-8'))
                if self.debug==1:
                    sys.stdout.write("Vou receber o número do tamanho da base de dados outra vez para certificar que está tudo direito\n")
                msgRecebida = connection.recv(1024)
                msg=msgRecebida.decode('utf-8')
                if self.debug==1:
                    sys.stdout.write(f"O número recebido foi {msg}\n")

                if int(msg)==self.tamanhoDataBase: 
                    nextStep=True

                else: 
                    nextStep=False
                    now = datetime.today().isoformat()
                    writeLogFile=logF(str(now),"EZ",address[0]+":"+str(6666),"SP",self.lista_logFile[0])
                    writeLogFile.escritaLogFile()

                if nextStep==True:
                    if self.debug==1:
                        sys.stdout.write("Como o número recebido foi o correto vou enviar as novas linhas da base de dados para o ss\n")
                    numeroLinhas=1
                    for it in dictDataBase.keys():
                        linhasType=dictDataBase.get(it)
                        for linha in linhasType:
                            stringResultado=str(numeroLinhas)+"-"+linha
                            connection.send(str(len(stringResultado)).encode('utf-8'))
                            connection.send(stringResultado.encode('utf-8'))
                            numeroLinhas+=1
                            stringResultado=""
                    if self.debug==1:
                        sys.stdout.write("Acabei de enviar todas as linhas novas da base de dados\n")
                    now = datetime.today().isoformat()
                    writeLogFile=logF(str(now),"ZT",address[0]+":"+str(6666),"SP",self.lista_logFile[0])
                    writeLogFile.escritaLogFile()

            else:
                now = datetime.today().isoformat()
                writeLogFile=logF(str(now),"EZ",address[0]+":"+str(6666),"SP",self.lista_logFile[0])
                writeLogFile.escritaLogFile()

        else:
            now = datetime.today().isoformat()
            writeLogFile=logF(str(now),"EZ",address[0]+":"+str(6666),"SP",self.lista_logFile[0])
            writeLogFile.escritaLogFile()
        lock.release()
            
    def runSP(self):
        """
        O path do ficheiro de dados do SP está armazenado na variável path_FileDataBase
        A lista com nome listaIP_SS tem armazenado os ips do SS para este SP          Exemplo:  IP-[10.0.1.10,10.0.2.10]
                                                                                                      |             |
        A lista com nome listaPorta_SS tem armazenado as portas do SS para este SP           Porta-[3333     ,   3333]
        A lista com nome listaLogFile tem os paths dos logs files do domain e de todos os dominios (all), basicamente é uma lista com prioridades
        Exemplo : [Files/logfileSP.txt,Files/logfiles.txt]
                 Log file do dominio do SP, Log file do all

        É nesta função que existe a junção e encadeamento das diversos processos existentes no SP
        A metodologia utilizada nesta função é a seguinte:
        1º Parsing de todos os ficheiros que são necessários para o arranque do componente 
        2º Preenchimento do ficheiro log com o comportamento do parsing e do arranque do componente
        3º Inicialização do processo de zone transfer entre os servidores 
        4º Inicialização do processo de resposta a queries dos clientes 

        DISCLAIMER: Depois de "inicializados" os processos de zone transfer e respostaa queries, o servidor está pronto a fazer estes processos
        """

        parseConfFile = parseConfigFile(self.nameConfig_File)
        listaIP_SS,listaPorta_SS,listaLogFile,pathFileDataBase = parseConfFile.parsingConfigFile()  
        self.listaIP_SS=listaIP_SS
        self.lista_logFile=listaLogFile

        if self.listaIP_SS==[] and self.lista_logFile==[] and listaPorta_SS==[] and pathFileDataBase=="":
            now = datetime.today().isoformat()
            writeLogFile=logF(str(now),"FL","127.0.0.1","Parse config File error",self.lista_logFile[0])
            writeLogFile.escritaLogFile()

        parseDFile = parseDataFile(dictDataBase, pathFileDataBase[:-1],self.lista_logFile)
        versao,tempoVerificacao,tamanhoDataBase=parseDFile.parsingDataFile()
        self.versao_DataBase=versao
        self.verifTime_DataBase=tempoVerificacao
        self.tamanhoDataBase=tamanhoDataBase
        now = datetime.today().isoformat()
        writeLogFile=logF(str(now),"EV","@",self.nameConfig_File+" "+pathFileDataBase+" "+self.lista_logFile[0],self.lista_logFile[0])
        writeLogFile.escritaLogFile()
        sck_UDP =socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        sck_UDP.bind((self.ipSP, self.portaUDP))

        if self.debug==1:
            sys.stdout.write(f"Estou à escuta no {self.ipSP}:{self.portaUDP}\n")
        threading.Thread(target=sp.runfstThread, args=(self,)).start()
        threading.Thread(target=thrResolver.runfstResolver, args=(self.domainServer,self.ipSP,3332,dictDataBase)).start()
        while True:

            msg_UDP,add_UDP = sck_UDP.recvfrom(1024)

            if self.debug==1:
                sys.stdout.write(msg_UDP.decode('utf-8'))

            proQuery_UDP = pQuery(msg_UDP.decode('utf-8'), self.domainServer)

            queryCheck_UDP=proQuery_UDP.processQuery(0)

            if (queryCheck_UDP==False):
                if self.debug==1:
                    sys.stdout.write("\nA query pedida não é válida\n")

            else:
                if self.debug==1:
                    sys.stdout.write(f"\nRecebi uma mensagem do cliente {add_UDP}\n")
                now = datetime.today().isoformat()
                writeLogFile=logF(str(now),"QR/QE",self.ipSP+":"+str(self.portaUDP),msg_UDP.decode('utf-8'),self.lista_logFile[0])
                writeLogFile.escritaLogFile()
                ansQuery = aQuery(proQuery_UDP.message_id,"R+A",str(0),dictDataBase,proQuery_UDP.typeValue)
                resposta = ansQuery.answerQuery()
                respostaDatagram = '\n'.join(resposta)
                b =respostaDatagram.encode('UTF-8')
                sck_UDP.sendto(b,add_UDP)
                now = datetime.today().isoformat()
                writeLogFile=logF(str(now),"RP\RR",add_UDP[0]+":"+str(self.portaUDP),respostaDatagram,self.lista_logFile[0])
                writeLogFile.escritaLogFile()

        sck_UDP.close()


def main():
    ipSP = sys.argv[1]
    nameConfig_File = sys.argv[2]  # ../Files/ConfigFileSP.txt 
    domainServer = sys.argv[3]
    debug=0
    if len(sys.argv)==5:
        debug=int(sys.argv[4])
    portaUDP = 3333
    portaTCP_SP = 4444
    portaTCP_SS = 6666
    spObj = sp(ipSP,domainServer,nameConfig_File,portaUDP,portaTCP_SP, portaTCP_SS,debug)
    spObj.runSP()    

if __name__ == "__main__":
    main()