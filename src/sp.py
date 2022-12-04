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

class sp:
    
    global dictDataBase              # Variável global que serve como estrutura de dados do SP
    dictDataBase=dict()              # Inicialização da estrutura de dados do SP
    global lock                      # Variável global para controlo de concorrência das threads na transferência de zona 
    lock = threading.Lock()          # Inicialização do Lock
    def __init__(self, ipSP, domainServer, nameConfig_File, portaUDP, portaTCP_SP, portaTCP_SS):
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

    def runfstThread(ipSP,portaTCP_SP,verifTime_DataBase,versao_DataBase,domainServer,listaIP_SS,tamanhoDataBase,lista_LogFile):
        """
        Esta função pertence á zone transfer
        A metodologia da função é a seguinte:
        1º Criação/Inicialização de um socket TCP para comunicação entre servidores
        2º Ciclo que serve para aceitar a conexão entre servidores e delega a outra thread o trabalho da zone transfer 

        Esta função serve como "centro de controlo" da zone transfer.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ipSP,portaTCP_SP))
        s.listen()
        
        while True:
            connection, address = s.accept()
            threading.Thread(target=sp.runsecThread,args=(ipSP,connection,address,versao_DataBase,domainServer,listaIP_SS,tamanhoDataBase,lista_LogFile,verifTime_DataBase)).start() 
        s.close()

    def runsecThread(ipSP,connection,address,versao_DataBase,domainServer,listaIP_SS,tamanhoDataBase,lista_LogFile,verifTime_DataBase):
        """
        Esta função é a função que realmente realiza trabalho na zone transfer, tal como receber queries TCP do SS e enviar respostas ás queries do SS.
        Como podemos visualizar, é criado um protocolo para a zone transfer entre servidores.
        A especificação do protocolo aqui estabelecido, encontra-se devidamente ilustrado no relatório da primeira fase do trabalho.
        """
        sys.stdout.write("Vou tratar da parte da ZT no SP\n")
        sys.stdout.write("Vou tratar da parte da ZT no SP\n")

        lock.acquire()
        sys.stdout.write("Vou receber a primeira mensagem\n")
        msgRecebida = connection.recv(1024)
        msg=msgRecebida.decode('utf-8')
        sys.stdout.write(f"A mensagem que recebi foi {msg}\n")

        if msg=="ZT":
            sys.stdout.write(f"Vou enviar a versão da minha base de dados\nA minha versão é esta {str(versao_DataBase)}\n")
            sys.stdout.write(f"O TTL da base de dados que vou enviar é este {verifTime_DataBase}\n")
            msgEnviar=str(versao_DataBase)+" "+str(verifTime_DataBase)
            connection.send(msgEnviar.encode('utf-8'))
            sys.stdout.write("Vou receber o domínio para o qual se pretende fazer a ZT\n")
            msgRecebida = connection.recv(1024)
            msg=msgRecebida.decode('utf-8')
            sys.stdout.write(f"O domínio que recebi foi este {msg}\n")

            if sp.verificaDomain(msg,domainServer)==True and sp.verificaipSS(address[0],listaIP_SS)==True:
                nextStep=True

            else: 
                nextStep=False
                now = datetime.today().isoformat()
                writeLogFile=logF(str(now),"EZ",address[0]+":"+str(6666),"SP",lista_LogFile[0])
                writeLogFile.escritaLogFile()
            sys.stdout.write(f"Foram feitas todas as verificações e o resultado das mesmas é {nextStep}\n")

            if nextStep==True:
                sys.stdout.write(f"Vou enviar o tamanho da base de dados\n")
                sys.stdout.write(f"O tamanho da base de dados é este {tamanhoDataBase}\n")
                msgEnviar=str(tamanhoDataBase)
                connection.send(msgEnviar.encode('utf-8'))
                sys.stdout.write("Vou receber o número do tamanho da base de dados outra vez para certificar que está tudo direito\n")
                msgRecebida = connection.recv(1024)
                msg=msgRecebida.decode('utf-8')
                sys.stdout.write(f"O número recebido foi {msg}\n")

                if int(msg)==tamanhoDataBase: 
                    nextStep=True

                else: 
                    nextStep=False
                    now = datetime.today().isoformat()
                    writeLogFile=logF(str(now),"EZ",address[0]+":"+str(6666),"SP",lista_LogFile[0])
                    writeLogFile.escritaLogFile()

                if nextStep==True:
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
                    sys.stdout.write("Acabei de enviar todas as linhas novas da base de dados\n")
                    now = datetime.today().isoformat()
                    writeLogFile=logF(str(now),"ZT",address[0]+":"+str(6666),"SP",lista_LogFile[0])
                    writeLogFile.escritaLogFile()

            else:
                now = datetime.today().isoformat()
                writeLogFile=logF(str(now),"EZ",address[0]+":"+str(6666),"SP",lista_LogFile[0])
                writeLogFile.escritaLogFile()

        else:
            now = datetime.today().isoformat()
            writeLogFile=logF(str(now),"EZ",address[0]+":"+str(6666),"SP",lista_LogFile[0])
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
        self.VerifTime_DataBase=tempoVerificacao
        self.tamanhoDataBase=tamanhoDataBase
        now = datetime.today().isoformat()
        writeLogFile=logF(str(now),"EV","@",self.nameConfig_File+" "+pathFileDataBase+" "+self.lista_logFile[0],self.lista_logFile[0])
        writeLogFile.escritaLogFile()
        sck_UDP =socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        
        sck_UDP.bind((self.ipSP, self.portaUDP))

        sys.stdout.write(f"Estou à escuta no {self.ipSP}:{self.portaUDP}\n")
        threading.Thread(target=sp.runfstThread, args=(self.ipSP,self.portaTCP_SP,self.VerifTime_DataBase,self.versao_DataBase,self.domainServer,self.listaIP_SS,self.tamanhoDataBase,self.lista_logFile)).start()

        while True:

            msg_UDP,add_UDP = sck_UDP.recvfrom(1024)

            sys.stdout.write(msg_UDP.decode('utf-8'))

            proQuery_UDP = pQuery(msg_UDP.decode('utf-8'), self.domainServer)

            queryCheck_UDP=proQuery_UDP.processQuery(0)

            if (queryCheck_UDP==False):
                sys.stdout.write("\nA query pedida não é válida\n")

            else:
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
    ipSP = '10.2.2.2' #ISTO AQUI TEM DE SER ALTERADO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    nameConfig_File = sys.argv[1]  # ../Files/ConfigFileSP.txt 
    domainServer = sys.argv[2]
    portaUDP = 3333
    portaTCP_SP = 4444
    portaTCP_SS = 6666
    spObj = sp(ipSP,domainServer,nameConfig_File,portaUDP,portaTCP_SP, portaTCP_SS)
    spObj.runSP()    

if __name__ == "__main__":
    main()