from re import T
import socket
from sys import argv
from datetime import datetime  
from parserConfFile import parseConfigFile
from parserDataFile import parseDataFile
from answerQuery import aQuery
from processQuery import pQuery

def answerQuery(dict_Data_Base,typeValue):
    # Precimos dos campos response-values(Por exemplo:MX), authorities-values(NS) e extra-values (A para ns e mx)
    listaRes=[]
    listaRespValues=dict_Data_Base[typeValue]
    listaAuthValues=dict_Data_Base["NS"]
    listaExtraValues=dict_Data_Base["A"]
    for it1 in listaRespValues:
        listaP=it1.split(' ')
        if(listaP[0]=='@'):
                listaRes.append(it1)
    for it2 in listaAuthValues:
        listaP=it2.split(' ')
        if(listaP[0]=='@'):
                listaRes.append(it2)
    for it3 in listaExtraValues:
        listaP=it3.split(' ')
        if(typeValue.lower() in listaP[0] or "ns" in listaP[0]):
                listaRes.append(it3)

    

    return listaRes
"""
import socket

def resposta(message):
    header=[]
    data=[]
    lines=message.split(' ')
    message_id=lines[0]
    flags="R+A"
    m="% s" % message_id
    zero="% s" % 0
    header.append(m)
    header.append(flags)
    header.append("% s" % 0)
    header.append("% s" % 0)
    header.append("% s" % 0)
    header.append("% s" % 0)
    data.append(lines[6])
    data.append(lines[7])
    reply=header+data
    ##procurar na base de dados
    strDatagram = ' '.join(reply)
    return strDatagram



def main():
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    endereco = "10.0.1.10"
    porta = 3333
    sck.bind((endereco, porta))

    print(f"Estou à escuta no {endereco}:{porta}")

    while True:
        msg,add = sck.recvfrom(1024)
        print(f"Recebi uma mensagem do cliente {add}")
        msg=msg.decode('UTF-8')
        print(msg)
        #Processa a mensagem e procura na BD
        reply=resposta(msg)
        sck.sendto(reply.encode('UTF-8'),add)

    sck.close()

if __name__ == "__main__":
    main()
from random import randint
import socket
from sys import argv


def main():
    # Abertura do socket de comunicação do cliente com os servidores
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Recolha dos parâmetros que o cliente precisa para enviar a query DNS
    
    endereco = "10.0.0.20"
    porta = 3333
    
    ip=argv[1]
    domain=argv[2]
    type=argv[3]
    recc=argv[4]
    # Fim da recolha
    # Criação do datagrama UDP para posterior envio 
    # Acrescentar parâmetros do cabeçalho e do data
    header=[]
    data=[]
    message_id=randint(1,65535)
    flags="Q+"+recc
    m="% s" % message_id
    zero="% s" % 0
    header.append(m)
    header.append(flags)
    header.append(zero)
    header.append(zero)
    header.append(zero)
    header.append(zero)
    data.append(domain)
    data.append(type)
    #data.append(NULL)
    #data.append(NULL)
    #data.append(NULL)
    # Fim do acrescento 
    datagramaUDPDesincriptada=header+data #Criação da mensagem(header+data)
    strDatagram = ' '.join(datagramaUDPDesincriptada)
    print("Estou a enviar esta mensagem",strDatagram)
    sck.sendto(strDatagram.encode('UTF-8'),(ip, 3333))
    
    while True:
        msg,add = sck.recvfrom(1024)
        print(f"Recebi uma mensagem do cliente {add}")
        print(msg.decode('UTF-8'))
    sck.close()

if __name__ == "__main__":
    main()
"""

     
def main():
    # O path do ficheiro de dados do SP está armazenado na variável path_FileDataBase
    # A lista com nome listaIP_SS tem armazenado os ips do SS para este SP          Exemplo:  IP-[10.0.1.10,10.0.2.10]
    #                                                                                              |             |
    # A lista com nome listaPorta_SS tem armazenado as portas do SS para este SP           Porta-[3333     ,   3333]
    # A lista com nome listaLogFile tem os paths dos logs files do domain e de todos os dominios (all), basicamente é uma lista com prioridades
    # Exemplo : [Files/logfileSP.txt,Files/logfiles.txt]
    #          Log file do dominio do SP, Log file do all

    nameConfig_File=argv[1]          # ../Files/ConfigFileSP.txt 
    domain_server=argv[2]
    parseConfFile = parseConfigFile(nameConfig_File)
    listaIP_SS,listaPorta_SS,listaLogFile,pathFileDataBase = parseConfFile.parsingConfigFile()  
    dictDataBase={}

    parseDFile = parseDataFile(dictDataBase, pathFileDataBase[:-1])
    parseDFile.parsingDataFile()
    

    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    enderecoSP = '10.0.1.10'
    portaSP = 3333
    
    sck.bind((enderecoSP, portaSP))

    print(f"Estou à escuta no {enderecoSP}:{portaSP}")

    while True:
        msg,add = sck.recvfrom(1024)
        print(msg.decode('utf-8'))
        proQuery = pQuery(msg.decode('utf-8'),domain_server)
        queryCheck,typeValue= proQuery.processQuery()
        if (queryCheck==False):
            print("A query pedida não é válida")
        else:
            print(f"Recebi uma mensagem do cliente {add}")
            f=open(listaLogFile[0],"a")  
            now = datetime.today().isoformat()
            lineLogFile="{"+str(now)+"} "+"{QR/QE}"+" {"+enderecoSP+":"+str(portaSP)+"} "+ "{"+msg.decode('utf-8')+"}\n"
            f.write(lineLogFile)
            f.close()
            ansQuery = aQuery(dictDataBase,typeValue)
            resposta = ansQuery.answerQuery()
            respostaDatagram = '\n'.join(resposta)
            b =respostaDatagram.encode('UTF-8')
            sck.sendto(b,add)

    sck.close()

if __name__ == "__main__":
    main()