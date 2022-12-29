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

class spReverse:
    global dictDataBase              # Variável global que serve como estrutura de dados do SP
    dictDataBase=dict()              # Inicialização da estrutura de dados do SP

    def __init__(self, ipSP, domainServer,portaUDP,nameConfig_File,modo):
        """
        Criação/Inicialização da classe sp
        """
        self.ipSP = ipSP
        self.domainServer = domainServer
        self.nameConfig_File = nameConfig_File
        self.portaUDP = portaUDP
        self.debug=modo

   
    def runSPReverse(self):
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

        parseConfFile = parseConfigFileSPRverse(self.nameConfig_File)
        listaLogFile,pathFileDataBase = parseConfFile.parsingConfigFile()  

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
    spObj = spReverse(ipSP,domainServer,portaUDP,nameConfig_File,debug)
    spObj.runSPReverse()    

if __name__ == "__main__":
    main()