# Started in: 31/09/2022
# Changed by: Gonçalo Braga, João Gonçalves and Miguel Senra
# Finished in: 23/11/2022
import messageDNS

class aQuery:
    def __init__(self,message_id,flags,response_code, dictDataBase, typeValue, domain):
        self.dictDataBase = dictDataBase
        self.domain = domain
        self.typeValue = typeValue
        self.message_id = message_id
        self.flags=flags
        self.response_code=response_code

    def answerQuery(self):
    # Precimos dos campos response-values(Por exemplo:MX), authorities-values(NS) e extra-values (A para ns e mx)
        listaRes=[]
        listaCabecalho=[]
        listaCabecalho.append("# Header")
        listaCabecalho.append("MESSAGE-ID = "+self.message_id+",FLAGS = "+self.flags+",RESPONSE-CODE = "+self.response_code)
        listaRespValues=self.dictDataBase[self.typeValue]
        nValues=0
        guardaResponseValues = ""
        listaAuthValues=self.dictDataBase["NS"]
        nAuth=0
        guardaAuthValues = ""
        listaExtraValues=self.dictDataBase["A"]
        nExtraValues=0
        guardaExtraValues = ""
        for it1 in listaRespValues:
            listaP=it1.split(' ')
            if(listaP[0]=='@'):
                    listaRes.append("RESPONSE-VALUES = "+it1)
                    guardaResponseValues += listaP
                    nValues+=1
        for it2 in listaAuthValues:
            listaP=it2.split(' ')
            if(listaP[0]=='@'):
                    listaRes.append("AUTHORITIES-VALUES = "+it2)
                    guardaAuthValues += listaP
                    nAuth+=1
        for it3 in listaExtraValues:
            listaP=it3.split(' ')
            if(self.typeValue.lower() in listaP[0] or "ns" in listaP[0]):
                    guardaExtraValues += listaP
                    listaRes.append("EXTRA-VALUES = " +it3)
                    nExtraValues+=1
        listaCabecalho.append("N-VALUES = "+str(nValues)+" , "+"N-AUTHORITIES ="+str(nAuth)+" , "+"N-EXTRA-VALUES ="+str(nExtraValues)+" ;")
        listaCabecalho.append("# Data: Query Info")
        listaCabecalho.append("QUERY-INFO.NAME = "+" @ ,"+" QUERY-INFO.TYPE = "+self.typeValue+" ;")
        listaCabecalho.append("# Data: List of Response, Authorities and Extra Values")
        
        m = messageDNS(self.message_id,self.flags,self.response_code,nValues,nAuth,nExtraValues,self.domain,self.typeValue,guardaResponseValues,guardaAuthValues,guardaExtraValues)
        m.serialize()

        return (listaCabecalho+listaRes) and m
