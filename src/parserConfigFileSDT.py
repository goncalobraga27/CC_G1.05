class parseConfigFileSDT:

  def __init__(self, configFile):
    self.configFile = configFile  
    

  def parsingConfigFile(self):
        file= open (self.configFile, "r")        
        lines =file.readlines()              
        file.close()    
        dic=dict()
        for line in lines:
            lista_Parametros=line.split(' ')
            if (lista_Parametros[0]!='#' and lista_Parametros[0]!='\n'):
                if(lista_Parametros[1]=='NS'):
                    dic[lista_Parametros[0]]=lista_Parametros[2]
        return (dic)