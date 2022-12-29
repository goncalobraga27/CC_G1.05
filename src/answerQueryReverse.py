# Started in: 31/09/2022
# Changed by: Gonçalo Braga, João Gonçalves and Miguel Senra
# Finished in: 23/11/2022

class aQueryReverse:
    def __init__(self,message_id,flags,response_code, dictDataBase, typeValue,ipADescobrir):
        self.dictDataBase = dictDataBase
        self.typeValue = typeValue
        self.ipADescobrir=ipADescobrir
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
        nValues=1
        for it1 in listaRespValues:
            linha=it1.split(' ')
            if(linha[0]==self.ipADescobrir):
                    listaRes.append("RESPONSE-VALUES = "+linha[2])

        listaCabecalho.append("N-VALUES = "+str(nValues)+" , "+"N-AUTHORITIES = 0" + " , "+"N-EXTRA-VALUES = 0;")
        listaCabecalho.append("# Data: Query Info")
        listaCabecalho.append("QUERY-INFO.NAME = "+" @ ,"+" QUERY-INFO.TYPE = "+self.typeValue+" ;")
        listaCabecalho.append("# Data: List of Response, Authorities and Extra Values")
        

        return (listaCabecalho+listaRes)