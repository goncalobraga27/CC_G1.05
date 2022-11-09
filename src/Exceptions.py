import re

class exceptions:
    def __init__(self):
        pass

    @staticmethod
    def validatePort(port):
        if 1<=port<=65535:
            return True
        else:
            return False
 
    @staticmethod
    def check(Ip): 
        regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        if(re.search(regex, Ip)): 
            return True  
        else: 
            return False

    