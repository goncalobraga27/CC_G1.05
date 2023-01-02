# Started in: 31/09/2022
# Changed by: Gonçalo Braga, João Gonçalves and Miguel Senra
# Finished in: 23/11/2022

from logFile import logF
from datetime import datetime

class parseDataFile:

    def __init__(self,dictDataBase,pathDataBase,lista_logFile):
        self.dictDataBase = dictDataBase
        self.pathDataBase = pathDataBase
        self.lista_logFile=lista_logFile

    def parsingDataFile(self):
        file=open(self.pathDataBase,"r")
        lines=file.readlines()
        file.close()
        tamanhofile=1
        versao_DataBase=-1
        VerifTime_DataBase=0
        for line in lines:
            linhaParametros=line.split(' ')
            if (linhaParametros[0]!='#' and linhaParametros[0]!='\n'):
                if (linhaParametros[1]=="DEFAULT"):
                        self.dictDataBase[linhaParametros[1]]=[]
                if (linhaParametros[1]=="SOASP"):
                        self.dictDataBase[linhaParametros[1]]=[]
                if (linhaParametros[1]=="SOAADMIN"):
                        self.dictDataBase[linhaParametros[1]]=[]
                if (linhaParametros[1]=="SOASERIAL"):
                        self.dictDataBase[linhaParametros[1]]=[]
                if (linhaParametros[1]=="SOAREFRESH"):
                        self.dictDataBase[linhaParametros[1]]=[]
                if (linhaParametros[1]=="SOARETRY"):
                        self.dictDataBase[linhaParametros[1]]=[]
                if (linhaParametros[1]=="SOAEXPIRE"):
                        self.dictDataBase[linhaParametros[1]]=[]
                if (linhaParametros[1]=="NS"):
                        self.dictDataBase[linhaParametros[1]]=[]
                if (linhaParametros[1]=="A"):
                        self.dictDataBase[linhaParametros[1]]=[]
                if (linhaParametros[1]=="CNAME"):
                        self.dictDataBase[linhaParametros[1]]=[]
                if (linhaParametros[1]=="MX"):
                        self.dictDataBase[linhaParametros[1]]=[]
                if (linhaParametros[1]=="PTR"):
                        self.dictDataBase[linhaParametros[1]]=[]
                tamanhofile+=1
        for line in lines:
            linhaParametros=line.split(' ')
            if (linhaParametros[0]!='#' and linhaParametros[0]!='\n'):
                if (linhaParametros[1]=="DEFAULT"):
                        self.dictDataBase[linhaParametros[1]].append(line[:-1])
                if (linhaParametros[1]=="SOASP"):
                        self.dictDataBase[linhaParametros[1]].append(line[:-1])
                if (linhaParametros[1]=="SOAADMIN"):
                        self.dictDataBase[linhaParametros[1]].append(line[:-1])
                if (linhaParametros[1]=="SOASERIAL"):
                        self.dictDataBase[linhaParametros[1]].append(line[:-1])
                if (linhaParametros[1]=="SOAREFRESH"):
                        self.dictDataBase[linhaParametros[1]].append(line[:-1])
                if (linhaParametros[1]=="SOARETRY"):
                        self.dictDataBase[linhaParametros[1]].append(line[:-1])
                if (linhaParametros[1]=="SOAEXPIRE"):
                        self.dictDataBase[linhaParametros[1]].append(line[:-1])
                if (linhaParametros[1]=="NS"):
                        self.dictDataBase[linhaParametros[1]].append(line[:-1])
                if (linhaParametros[1]=="A"):
                        self.dictDataBase[linhaParametros[1]].append(line[:-1])
                if (linhaParametros[1]=="CNAME"):
                        self.dictDataBase[linhaParametros[1]].append(line[:-1])
                if (linhaParametros[1]=="MX"):
                        self.dictDataBase[linhaParametros[1]].append(line[:-1])
                if (linhaParametros[1]=="PTR"):
                        self.dictDataBase[linhaParametros[1]].append(line[:-1])
        linha=self.dictDataBase["SOASERIAL"]
        linhaD=linha[0].split(' ')[2]
        versao_DataBase=linhaD
        linha=self.dictDataBase["SOAREFRESH"]
        linhaD=linha[0].split(' ')[2]
        VerifTime_DataBase=linhaD
        if self.dictDataBase=={}:
                now = datetime.today().isoformat()
                writeLogFile=logF(str(now),"FL","127.0.0.1","Parse Data File error",self.lista_logFile[0])
                writeLogFile.escritaLogFile()

        return versao_DataBase,VerifTime_DataBase,tamanhofile
