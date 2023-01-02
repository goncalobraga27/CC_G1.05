from entryCache import entry
class aQuerySR:
    def __init__(self,message_id,flags,response_code, cache, typeValue,domain):
        self.cache = cache
        self.typeValue = typeValue
        self.message_id = message_id
        self.flags=flags
        self.response_code=response_code
        self.domain=domain
    def answerQuerySR(self):
        listaRes=[]
        listaCabecalho=[]
        listaCabecalho.append("# Header")
        listaRespValues=aQuerySR.giveResponse(self)
        if listaRespValues !=[]:
            listaCabecalho.append("MESSAGE-ID = "+self.message_id+",FLAGS = "+self.flags+",RESPONSE-CODE = "+self.response_code)
        else : 
            listaCabecalho.append("MESSAGE-ID = "+self.message_id+",FLAGS = "+self.flags+",RESPONSE-CODE = "+"1")
        nValues=0
        for it1 in listaRespValues:
            listaRes.append("RESPONSE-VALUES = "+it1)
            nValues+=1
        listaCabecalho.append(("N-VALUES = "+str(nValues))+" ;")
        listaCabecalho.append("# Data: Query Info")
        listaCabecalho.append("QUERY-INFO.NAME = "+self.domain+","+" QUERY-INFO.TYPE = "+self.typeValue+" ;")
        listaCabecalho.append("# Data: List of Response, Authorities and Extra Values")
        

        return (listaCabecalho+listaRes)
    
    def giveResponse(self):
        listaResultado=[]
        for key in self.cache.keys():
            eR=self.cache[key]
            if(eR.name==self.domain and eR.type==self.typeValue):
                listaResultado.append(eR.value)
            else:
                return []
        return listaResultado
    
    def canGiveResponse(self):
        for key in self.cache.keys():
            e=self.cache[key]
            if(e.name==self.domain and e.type==self.typeValue):
                return True
        return False


