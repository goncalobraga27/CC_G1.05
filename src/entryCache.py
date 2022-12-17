
class entry:
    def __init__(self,name,type,value,ttl,order,origin,timestamp,index,status):
        self.name=name
        self.type=type
        self.value=value
        self.ttl=ttl
        self.order=order
        self.origin=origin
        self.timestamp=timestamp
        self.index=index
        self.status=status

    def stringEntry(self):
        result=""
        result+="Name: "+self.name+"\n"
        result+="Type: "+self.type+"\n"
        result+="Value: "+self.value+"\n"
        result+="TTL: "+str(self.ttl)+"\n"
        result+="Order: "+self.order+"\n"
        result+="Origin: "+self.origin+"\n"
        result+="TimeStamp: "+str(self.timestamp)+"\n"
        result+="Index: "+str(self.index)+"\n"
        result+="Status: "+self.status+"\n\n\n"
        return result

    def setIndex(self,numero):
        self.index=numero
    
    def getTTL(self):
        return self.ttl
    
    def getTimeStamp(self):
        return self.timestamp



    
