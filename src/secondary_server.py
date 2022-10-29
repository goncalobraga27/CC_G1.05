import socket
from sys import argv

def main():
    nameConfig_File=argv[1]
    #file= open (nameConfig_File, "r")         # Abertura do ConfigFile
    #lines =file.readlines()              
    #file.close()            
    
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    endereco = "10.0.2.10"
    porta = 3333
    sck.bind((endereco, porta))

    print(f"Estou à escuta no {endereco}:{porta}")

    while True:
        msg,add = sck.recvfrom(1024)
        print(msg.decode('utf-8'))
        print(f"Recebi uma mensagem do cliente {add}")

    sck.close()



if __name__ == "__main__":
    main()