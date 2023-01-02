import socket
import sys
import threading
import time
from datetime import datetime,timedelta
from re import T
from entryCache import entry

class thrCache:

    def runControlCache(c): 
        lock = threading.Lock()
        lock.acquire()
        while True:
            for key in c.cache.keys():
                e=c.cache[key]
                ttl=e.getTTL()
                timestamp=e.getTimeStamp()
                time=datetime.now()-timedelta(seconds=int(ttl))
                if time>timestamp:
                    c.cache[key]=entry("","","","","","","",key,"FREE")
        lock.release()

        