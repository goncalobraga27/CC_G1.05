from random import randint
import socket
from sys import argv

class cl:

    def __init__(self, ipServer, domain, type, recc):
        self.ipServer = ipServer
        self.domain = domain
        self.type = type
        self.recc = recc

    def runCL(self):
        # Abertura do socket de comunicação do cliente com os servidores
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Recolha dos parâmetros que o cliente precisa para enviar a query DNS

        # Fim da recolha
        # Criação do datagrama UDP para posterior envio 
        # Acrescentar parâmetros do cabeçalho e do data
        header=[]
        data=[]
        message_id=randint(1,65535)
        flags="Q+"+self.recc
        m="% s" % message_id
        zero="% s" % 0
        header.append(m)
        header.append(flags)
        header.append(zero)
        header.append(zero)
        header.append(zero)
        header.append(zero)
        data.append(self.domain)
        data.append(self.type)
        #data.append(NULL)
        #data.append(NULL)
        #data.append(NULL)
        # Fim do acrescento 
        datagramaUDPDesincriptada=header+data #Criação da mensagem(header+data)
        strDatagram = ' '.join(datagramaUDPDesincriptada)

        if len(strDatagram) <= 1000: #Ver se o tamanho da mensagem é menor ou igual a 1000 bytes
            print("Estou a enviar esta mensagem",strDatagram)
            b = strDatagram.encode('UTF-8')
            sck.sendto(b, (self.ipServer, 3333))

        msg=""

        while msg=="":
            msg,add=sck.recvfrom(1024)
            print(f"Recebi uma mensagem do servidor{add}")
            print("CONTEÚDO DA MENSAGEM:\n")
            print(msg.decode('utf-8'))

        sck.close()

def main():
    ipServer = argv[1]
    domain = argv[2]
    type = argv[3]
    recc = argv[4]
    clObj = cl(ipServer,domain,type,recc)
    clObj.runCL()

if __name__ == '__main__':
    main()