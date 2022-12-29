# Started in: 31/09/2022
# Changed by: Gonçalo Braga, João Gonçalves and Miguel Senra
# Finished in: 23/11/2022

from random import randint
import socket
from sys import argv
from datetime import datetime
import time
from logFile import logF
from messageDNS import MessageDNS
import sys


class cl:

    def __init__(self, ipServer, domain, type, recc,logFile,modo):
        self.ipServer = ipServer
        self.domain = domain
        self.type = type
        self.recc = recc
        self.logF = logFile
        self.debug = modo

    def runCL(self):
        
        """
        O ip do Servidor à qual se quer enviar a query, o seu domínio, o tipo da mensagem, a flag e o path do log File são passados como argumento
        no objeto que é passado como argumento na função. 

        A metodologia utilizada nesta função é a seguinte:
            1º É aberto um socket de comunicação UDP
            2º É criado um datagrama UDP desincriptado com os dados da query
            3º É enviada a mensagem se o tamanho for menor que 1000 bytes
            4º É recebida a resposta por parte do Servidor
            5º O socket UDP é encerrado
        """

        now = datetime.today().isoformat()
        writeLogFile=logF(str(now),"EV","@",self.logF,self.logF)
        writeLogFile.escritaLogFile()
        # Abertura do socket de comunicação do cliente com os servidores
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sck.settimeout(5)
        # Recolha dos parâmetros que o cliente precisa para enviar a query DNS

        # Fim da recolha
        # Criação do datagrama UDP para posterior envio 
        # Acrescentar parâmetros do cabeçalho e do data
        message_id=randint(1,65535)
        flags = "Q+"+self.recc
        response_code = 0
        numberOfValues = 0
        numberOfAuthorities = 0
        numberOfExtraValues = 0
        domain = self.domain
        type = self.type
        responseValues = None
        authoritiesValues = None
        extraValues = None

        m = str(message_id) + flags + str(response_code) + str(numberOfValues) + str(numberOfAuthorities) + str(numberOfExtraValues) + domain + type

        if int(numberOfValues) > 0:
            m += responseValues
        if int(numberOfAuthorities) > 0:
            m += authoritiesValues  
        if int(numberOfExtraValues) > 0:
            m+= extraValues 

        msg = MessageDNS(message_id,flags,response_code,numberOfValues,numberOfAuthorities,numberOfExtraValues,domain,type,responseValues,authoritiesValues,extraValues)
        
        b = msg.serialize()

        if self.debug==1:
            sys.stdout.write("Estou a enviar esta mensagem\n")
        
        sck.sendto(b, (self.ipServer, 3333))
        
        now = datetime.today().isoformat()
        writeLogFile=logF(str(now),"QR/QE","localHost:"+str(3333),m,self.logF)
        writeLogFile.escritaLogFile()
        
        # Resposta ás queries pedidas
        m,add=sck.recvfrom(1024)
        if self.debug==1:
            sys.stdout.write(f"Recebi uma mensagem do servidor{add}\n")
            sys.stdout.write("CONTEÚDO DA MENSAGEM:\n")
            
        m = msg.deserialize(m)
        
        imprime = m + "\n"
        
        if self.debug==1:
            sys.stdout.write(imprime)
        now = datetime.today().isoformat()
        writeLogFile=logF(str(now),"RP/RR","localHost:"+str(3333),m,self.logF)
        writeLogFile.escritaLogFile()

        sck.close()

def main():
    ipServer = argv[1]
    domain = argv[2]
    type = argv[3]
    recc = argv[4]
    debug=0
    if len(argv)==6:
        debug=int(argv[5])
    clObj = cl(ipServer,domain,type,recc,"../Files/logfileCL.txt",debug)
    clObj.runCL()

if __name__ == '__main__':
    main()