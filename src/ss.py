from datetime import datetime
import socket
from sys import argv

def parsingConfigFile(nameConfig_File):
    file= open (nameConfig_File, "r")        
    lines =file.readlines()              
    file.close()    
    listaIP_SP=[]
    listaPorta_SP=[]
    listaLogFile=[]   
    path_FileDataBase=""
    for line in lines:
        lista_Parametros=line.split(' ')
        if (lista_Parametros[0]!='#' and lista_Parametros[0]!='\n'):
            if(lista_Parametros[1]=='DB'):
                path_FileDataBase=lista_Parametros[2]
            if(lista_Parametros[1]=='SP'):
                lista_IP_Porta=lista_Parametros[2].split(':')
                listaIP_SP.append(lista_IP_Porta[0])
                listaPorta_SP.append(int(lista_IP_Porta[1]))
            if(lista_Parametros[1]=='LG'):
                listaLogFile.append(lista_Parametros[2][:-1])
    return (listaIP_SP,listaPorta_SP,listaLogFile,path_FileDataBase)

def processQuery(msg,domain_server):
    query=str(msg)
    queryCheck=True
    lista_ParametrosQuery=query.split(' ')
    if (int(lista_ParametrosQuery[0])>1 and int(lista_ParametrosQuery[0])<65535):
        queryCheck=True
    else:
        return False
    lista_Flags=lista_ParametrosQuery[1].split('+')
    for it in lista_Flags:
        if (it=='R' or it=='Q' or it=='A'):
            queryCheck=True
        else:
            return False
    if(lista_ParametrosQuery[2]=='0' and lista_ParametrosQuery[3]=='0' and lista_ParametrosQuery[4]=='0' and lista_ParametrosQuery[5]=='0'):
            queryCheck=True
    else:
            return False
    if (lista_ParametrosQuery[6]==domain_server):
        queryCheck=True
    else:
        return False
    if (lista_ParametrosQuery[7]=='DEFAULT' or lista_ParametrosQuery[7]=='SOASP' or lista_ParametrosQuery[7]=='SOAADMIN' or\
        lista_ParametrosQuery[7]=='SOASERIAL' or  lista_ParametrosQuery[7]=='SOAREFRESH' or  lista_ParametrosQuery[7]=='SOARETRY' or\
        lista_ParametrosQuery[7]=='SOAEXPIRE' or lista_ParametrosQuery[7]=='NS' or lista_ParametrosQuery[7]=='A' or\
        lista_ParametrosQuery[7]=='CNAME' or lista_ParametrosQuery[7]=='MX' or lista_ParametrosQuery[7]=='PTR' ):
                    queryCheck=True
    else:
            return False
    
    return(queryCheck,int(lista_ParametrosQuery[0]))
    


def main():
    nameConfig_File=argv[1]       #  ../Files/ConfigFileSS.txt 
    domain=argv[2]
    listaIP_SP,listaPorta_SP,listaLogFile,path_FileDataBase=parsingConfigFile(nameConfig_File)    
    # O path do ficheiro de dados do SS está armazenado na variável path_FileDataBase
    # A lista com nome listaIP_SP tem armazenado o ips do SP para este SS         Exemplo:  IP-[10.0.1.10]
    #                                                                                              |   
    # A lista com nome listaPorta_SP tem armazenado as portas do SP para este SS         Porta-[3333]
    # A lista com nome listaLogFile tem os paths dos logs files do domain e de todos os dominios (all), basicamente é uma lista com prioridades
    # Exemplo : [Files/logfileSS.txt,Files/logfiles.txt]
    #          Log file do dominio do SS, Log file do all
    
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    endereco = "10.0.2.10"
    porta = 3333
    sck.bind((endereco, porta))

    print(f"Estou à escuta no {endereco}:{porta}")

    while True:
        msg,add = sck.recvfrom(1024)
        print(msg.decode('utf-8'))
        if(processQuery(msg.decode('utf-8'),domain)==False):
            print("A query pedida não é válida")
        else:
            print(f"Recebi uma mensagem do cliente {add}")
            f=open(listaLogFile[0],"a")  
            now = datetime.today().isoformat()
            lineLogFile="{"+str(now)+"} "+"{QR/QE}"+" {"+endereco+":"+str(porta)+"} "+ "{"+msg.decode('utf-8')+"}\n"
            print(lineLogFile)
            f.write(lineLogFile)
            f.close()

    sck.close()



if __name__ == "__main__":
    main()