from datetime import datetime
import socket
from sys import argv
from processQuery import pQuery
from parserConfFile import parseConfigFile
from answerQuery import aQuery
from parserDataFile import parseDataFile

class ss:

    def __init__(self, ipSS, domain, nameConfig_File, portaUDP, portaTCP):
        self.nameConfig_File = nameConfig_File
        self.domain = domain
        self.ipSS = ipSS
        self.portaUDP = portaUDP
        self.portaTCP = portaTCP

    """
    def zoneTransferSS:
        abrir socket
        meter socket à escuta
        construir query para trasferencia de zona
        enviar query para pedir permissão
        recebe query com numero de linhas do ficheiro da BD
        Ver se tem permissão para iniciar a transferencia de zona
        SS teve autorização do SP para iniciar a transferência e vai iniciar transferencia de zona
    """

    def runSS(self):
        parseConfFile = parseConfigFile(self.nameConfig_File)
        listaIP_SP,listaPorta_SP,listaLogFile,path_FileDataBase=parseConfFile.parsingConfigFile()   
        # O path do ficheiro de dados do SS está armazenado na variável path_FileDataBase
        # A lista com nome listaIP_SP tem armazenado o ips do SP para este SS         Exemplo:  IP-[10.0.1.10]
        #                                                                                              |   
        # A lista com nome listaPorta_SP tem armazenado as portas do SP para este SS         Porta-[3333]
        # A lista com nome listaLogFile tem os paths dos logs files do domain e de todos os dominios (all), basicamente é uma lista com prioridades
        # Exemplo : [Files/logfileSS.txt,Files/logfiles.txt]
        #          Log file do dominio do SS, Log file do all
        
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dictDataBase={}

        #parseDFile = parseDataFile(dictDataBase, path_FileDataBase[:-1])
        #parseDFile.parsingDataFile()

        sck.bind((self.ipSS, self.portaUDP))

        print(f"Estou à escuta no {self.ipSS}:{self.portaUDP}")

        while True:
            msg,add = sck.recvfrom(1024)
            print(msg.decode('utf-8'))
            proQuery = pQuery(msg.decode('utf-8'),self.domain)
            queryCheck,typeValue= proQuery.processQuery()
            if(queryCheck==False):
                print("A query pedida não é válida")
            else:
                print(f"Recebi uma mensagem do cliente {add}")
                f=open(listaLogFile[0],"a")  
                now = datetime.today().isoformat()
                lineLogFile="{"+str(now)+"} "+"{QR/QE}"+" {"+self.ipSS+":"+str(self.portaUDP)+"} "+ "{"+msg.decode('utf-8')+"}\n"
                print(lineLogFile)
                f.write(lineLogFile)
                f.close()
                ansQuery = aQuery(dictDataBase,typeValue)
                resposta = ansQuery.answerQuery()
                respostaDatagram = '\n'.join(resposta)
                b =respostaDatagram.encode('UTF-8')
                sck.sendto(b,add)

        sck.close()

def main():
    ipSS = '10.0.0.11'
    nameConfig_File = argv[1]  # ../Files/ConfigFileSS.txt 
    domainServer = argv[2]
    portaUDP = 3333
    portaTCP = 6300
    ssObj = ss(ipSS,domainServer,nameConfig_File,portaUDP,portaTCP)
    ssObj.runSS()  

if __name__ == '__main__':
    main()
