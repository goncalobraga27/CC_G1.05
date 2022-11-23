# Started in: 31/09/2022
# Changed by: Gonçalo Braga, João Gonçalves and Miguel Senra
# Finished in: 23/11/2022

class logF:
    def __init__(self,date_SO,tipoentrada,ipPorta,dadosEntrada,path_FileLog):
        self.data=date_SO
        self.tipoEntrada=tipoentrada
        self.ipPorta=ipPorta
        self.dadosEntrada=dadosEntrada
        self.pathFileLog=path_FileLog
    
    def escritaLogFile(self):
        f=open(self.pathFileLog,"a")
        lineLogFile="{ "+self.data+" "+self.tipoEntrada+" "+self.ipPorta+" "+self.dadosEntrada+" }\n"
        f.write(lineLogFile)
        f.close()