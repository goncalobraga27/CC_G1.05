class parseConfigFileSR:

  def __init__(self, configFile):
    self.configFile = configFile  
    

  def parsingConfigFile(self):
        file= open (self.configFile, "r")        
        lines =file.readlines()              
        file.close()    
        listaIP_SP=[]
        listaPorta_SP=[]
        listaLogFile=[]   
        listaIPST=[]
        listaPortaST=[]
        contador=0
        for line in lines:
            lista_Parametros=line.split(' ')
            if (lista_Parametros[0]!='#' and lista_Parametros[0]!='\n'):
                if(lista_Parametros[1]=='LG'):
                    listaLogFile.append(lista_Parametros[2])
                if (lista_Parametros[1]=='DD'):
                    if(contador==0):
                        listaP=lista_Parametros[2].split(':')
                        listaIP_SP.append(listaP[0])
                        listaPorta_SP.append(listaP[1][:-1])
                        contador=contador+1
                    else:
                        listaP=lista_Parametros[2].split(':')
                        listaIPST.append(listaP[0])
                        listaPortaST.append(listaP[1][:-1])
                        contador=contador+1
        return (listaIP_SP,listaPorta_SP,listaLogFile,listaIPST,listaPortaST)