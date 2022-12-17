
import socket
import sys
import threading
import time
from datetime import datetime
from re import T


class thrResolver:

    def runfstResolver(domainServer,ipSP,porta,dictDataBase): # Thread utilizada no sp para atender pedidos do sr 
        lock = threading.Lock()
        lock.acquire()
        sck_UDP =socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        sck_UDP.bind((ipSP,porta))
        while True:
            msg_UDP,add_UDP = sck_UDP.recvfrom(1024)
            tipoPedido=msg_UDP.decode('utf-8')
            listaResultado=dictDataBase[tipoPedido]
            sck_UDP.sendto(str(len(listaResultado)).encode('UTF-8'),add_UDP)
            listaTypeDefault=dictDataBase["DEFAULT"]
            sck_UDP.sendto(listaTypeDefault[1].encode('UTF-8'),add_UDP)
            for linhaDataBase in listaResultado:
                sck_UDP.sendto((domainServer+" "+linhaDataBase).encode('UTF-8'),add_UDP)
        lock.release()

        


            



