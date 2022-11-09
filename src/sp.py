from re import T
import socket
from sys import argv
from datetime import datetime  
from parserConfFile import parseConfigFile
from parserDataFile import parseDataFile
from answerQuery import aQuery
from processQuery import pQuery
import threading
import time

class sp:

    def __init__(self, ipSP, domainServer, nameConfig_File, portaUDP, portaTCP_SP, portaTCP_SS, dictDataBase):
        self.ipSP = ipSP
        self.domainServer = domainServer
        self.nameConfig_File = nameConfig_File
        self.portaUDP = portaUDP
        self.portaTCP_SP = portaTCP_SP
        self.portaTCP_SS = portaTCP_SS
        self.dictDataBase = dictDataBase
        

    def zoneTransferSP(self): #incompleto...
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP

        databaseSP = open("../Files/databaseSP.txt", "r")

        s.bind((self.ipSP,self.portaTCP_SP))
        s.listen()

        print(f"Estou à escuta no {self.ipSP}:{self.portaTCP_SP}")

        while True:
            conn, address = s.accept()

            msg = conn.recv(1024)

            if not msg:
                break

            msg = msg.decode('utf-8')

            proQuery = pQuery(msg,self.domainServer)
            queryCheck = proQuery.processQuery()

            if proQuery.typeValue == 'SOASERIAL' and queryCheck == True:

                linhas = databaseSP.readlines()

                for linha in linhas:
                    s.sendall(str(linha))

        s.close()

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

        parseDFile = parseDataFile(self.dictDataBase, pathFileDataBase[:-1])
        parseDFile.parsingDataFile()
        

        sck_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        
        sck_UDP.bind((self.ipSP, self.portaUDP))

        print(f"Estou à escuta no {self.ipSP}:{self.portaUDP}\n")

        while True:
            msg_UDP,add_UDP = sck_UDP.recvfrom(1024)

            print(msg_UDP.decode('utf-8'))

            proQuery_UDP = pQuery(msg_UDP.decode('utf-8'), self.domainServer)

            queryCheck_UDP=proQuery_UDP.processQuery(0)

            if (queryCheck_UDP==False):
                print("A query pedida não é válida")

            else:
                print(f"Recebi uma mensagem do cliente {add_UDP}")
                f=open(listaLogFile[0],"a")  
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