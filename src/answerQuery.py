class aQuery:
    def __init__(self, dictDataBase, typeValue):
        self.dictDataBase = dictDataBase
        self.typeValue = typeValue

    def answerQuery(self):
        # Precimos dos campos response-values(Por exemplo:MX), authorities-values(NS) e extra-values (A para ns e mx)
        listaRes=[]
        listaRespValues=self.dictDataBase[self.typeValue]
        listaAuthValues=self.dictDataBase["NS"]
        listaExtraValues=self.dictDataBase["A"]
        for it1 in listaRespValues:
            listaP=it1.split(' ')
            if(listaP[0]=='@'):
                    listaRes.append(it1)
        for it2 in listaAuthValues:
            listaP=it2.split(' ')
            if(listaP[0]=='@'):
                    listaRes.append(it2)
        for it3 in listaExtraValues:
            listaP=it3.split(' ')
            if(self.typeValue.lower() in listaP[0] or "ns" in listaP[0]):
                    listaRes.append(it3)

        

        return listaRes