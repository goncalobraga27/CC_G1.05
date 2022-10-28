import socket
from sys import argv

def main():
    #### Leitura do ficheiro de configuração do SP
    nameConfig_File=argv[1]          # Files/ConfigFileSP.txt
    file= open (nameConfig_File, "r")        
    lines =file.readlines()              
    file.close()       
    linhasTratadas=0  
    listaIP_SS=[]
    listaPorta_SS=[]
    listaLogFile=[]
    path_FileDataBase=""
    #### Fim da leitura do ficheiro de configuração do SP
    #### Parsing do config file do SP
    for line in lines:
        lista_Parametros=line.split(' ')
        if (lista_Parametros[0]!='#' and lista_Parametros[0]!='\n'):
            if(lista_Parametros[1]=='DB'):
                path_FileDataBase=lista_Parametros[2]
            if(lista_Parametros[1]=='SS'):
                lista_IP_Porta=lista_Parametros[2].split(':')
                listaIP_SS.append(lista_IP_Porta[0])
                listaPorta_SS.append(int(lista_IP_Porta[1]))
            if(lista_Parametros[1]=='LG'):
                listaLogFile.append(lista_Parametros[2][:-1])
    print(listaLogFile)
   # O path do ficheiro de dados está armazenado na variável path_FileDataBase
   # A lista com nome listaIP_SS tem armazenado os ips do SS para este SP          Exemplo:  IP-[10.0.1.10,10.0.2.10]
   #                                                                                              |             |
   # A lista com nome listaPorta_SS tem armazenado as portas do SS para este SP           Porta-[3333     ,   3333]
   # A lista com nome listaLogFile tem os paths dos logs files do domain e de todos os dominios (all), basicamente é uma lista com prioridades
   # Exemplo : [Files/logfileSP.txt,Files/logfiles.txt]
   #          Log file do dominio do SP, Log file do all
   #### Fim do Parsing do config file do SP 


    


    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    enderecoSP = "10.0.1.10"
    portaSP = 3333
    
    sck.bind((enderecoSP, portaSP))

    print(f"Estou à escuta no {enderecoSP}:{portaSP}")

    while True:
        msg,add = sck.recvfrom(1024)
        print(msg.decode('utf-8'))
        print(f"Recebi uma mensagem do cliente {add}")

    sck.close()

if __name__ == "__main__":
    main()