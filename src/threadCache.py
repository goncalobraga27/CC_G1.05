import socket
import sys
import threading
import time
from datetime import datetime
from datetime import timedelta
from re import T
from entryCache import entry

class thrCache:

    def runControlCache(c): # Thread utilizada no sp para atender pedidos do sr 
        lock = threading.Lock()
        lock.acquire()
        while True:
            for key in c.cache.keys():
                e=c.cache[key]
                ttl=e.getTTL()
                timestamp=e.getTimeStamp()
                updatedTime=(datetime(timestamp)+timedelta(seconds=ttl))
                print(type(updatedTime))
                if updatedTime!=datetime.now():
                    c.cache[key]=entry("","","","","","","",key,"FREE")
        lock.release()

        