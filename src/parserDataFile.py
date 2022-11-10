class parseDataFile:

    def __init__(self, dictDataBase, pathDataBase):
        self.dictDataBase = dictDataBase
        self.pathDataBase = pathDataBase

    def parsingDataFile(self):
        file=open(self.pathDataBase,"r")
        lines=file.readlines()
        file.close()
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
        linhaD=linha.pop().split(' ')
        versao_DataBase=int(linhaD[2])
        linha=self.dictDataBase["SOAREFRESH"]
        linhaD=linha.pop().split(' ')
        VerifTime_DataBase=int(linhaD[2])

        return versao_DataBase,VerifTime_DataBase
