class parseConfigFileST:

  def __init__(self, configFile):
    self.configFile = configFile  
    

  def parsingConfigFile(self):
        file= open (self.configFile, "r")        
        lines =file.readlines()              
        file.close()    
        mainDomain=""   
        ipSDT=""
        portaSDT=""
        for line in lines:
            lista_Parametros=line.split(' ')
            if (lista_Parametros[0]!='#' and lista_Parametros[0]!='\n'):
                if(lista_Parametros[1]=='DD'):
                    mainDomain=lista_Parametros[0]
                    listaP=lista_Parametros[2].split(':')
                    ipSDT=listaP[0]
                    portaSDT=listaP[1]
                if(lista_Parametros[1]=='NS'):
                    mainDomain=lista_Parametros[0]
                    listaP=lista_Parametros[2].split(':')
                    ipSDT=listaP[0]
                    portaSDT=listaP[1]
        return (mainDomain,ipSDT,portaSDT)