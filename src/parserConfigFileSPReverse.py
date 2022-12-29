# Started in: 31/09/2022
# Changed by: Gonçalo Braga, João Gonçalves and Miguel Senra
# Finished in: 23/11/2022

from logFile import logF
from datetime import datetime

class parseConfigFileReverse:

  def __init__(self, configFile):
    self.configFile = configFile  
    

  def parsingConfigFile(self):
        file= open (self.configFile, "r")        
        lines =file.readlines()              
        file.close()    
        listaIP_SS=[]
        listaPorta_SS=[]
        listaLogFile=[]   
        path_FileDataBase=""
        for line in lines:
            lista_Parametros=line.split(' ')
            if (lista_Parametros[0]!='#' and lista_Parametros[0]!='\n'):
                if(lista_Parametros[1]=='DB'):
                    path_FileDataBase=lista_Parametros[2]
                if(lista_Parametros[1]=='LG'):
                    listaLogFile.append(lista_Parametros[2][:-1])
        return (listaLogFile,path_FileDataBase)