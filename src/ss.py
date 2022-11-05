from datetime import datetime
import socket
from sys import argv
from processQuery import pQuery
from parserConfFile import parseConfigFile
from answerQuery import aQuery
from parserDataFile import parseDataFile
def main():
    nameConfig_File=argv[1]       #  ../Files/ConfigFileSS.txt 
    domain=argv[2]
    parseConfFile = parseConfigFile(nameConfig_File)
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

    endereco = "10.0.2.10"
    porta = 3333
    sck.bind((endereco, porta))

    print(f"Estou à escuta no {endereco}:{porta}")

    while True:
        msg,add = sck.recvfrom(1024)
        print(msg.decode('utf-8'))
        proQuery = pQuery(msg.decode('utf-8'),domain)
        queryCheck,typeValue= proQuery.processQuery()
        if(queryCheck==False):
            print("A query pedida não é válida")
        else:
            print(f"Recebi uma mensagem do cliente {add}")
            f=open(listaLogFile[0],"a")  
            now = datetime.today().isoformat()
            lineLogFile="{"+str(now)+"} "+"{QR/QE}"+" {"+endereco+":"+str(porta)+"} "+ "{"+msg.decode('utf-8')+"}\n"
            print(lineLogFile)
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