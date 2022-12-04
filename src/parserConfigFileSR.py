class parseConfigFileSR:

  def __init__(self, configFile):
    self.configFile = configFile  
    

  def parsingConfigFile(self):
        file= open (self.configFile, "r")        
        lines =file.readlines()              
        file.close()    
        listaIP_SS=[]
        listaPorta_SS=[]
        listaIP_SP=[]
        listaPorta_SP=[]
        listaLogFile=[]   
        for line in lines:
            lista_Parametros=line.split(' ')
            if (lista_Parametros[0]!='#' and lista_Parametros[0]!='\n'):
                if(lista_Parametros[1]=='SS'):
                    lista_IP_Porta=lista_Parametros[2].split(':')
                    listaIP_SS.append(lista_IP_Porta[0])
                    listaPorta_SS.append(int(lista_IP_Porta[1]))
                if(lista_Parametros[1]=='SP'):
                    lista_IP_Porta=lista_Parametros[2].split(':')
                    listaIP_SP.append(lista_IP_Porta[0])
                    listaPorta_SP.append(int(lista_IP_Porta[1]))
                if(lista_Parametros[1]=='LG'):
                    listaLogFile.append(lista_Parametros[2])
        return (listaIP_SS,listaPorta_SS,listaIP_SP,listaPorta_SP,listaLogFile)