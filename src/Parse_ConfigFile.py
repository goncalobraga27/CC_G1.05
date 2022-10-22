# Objetivo : Ler um ficheiro .txt e guardá-lo numa estrutura de dados (neste caso um dicionário)
def main ():
    file= open ("configfileSP.txt", "r")         # Abertura do file
    lines =file.readlines()                      # Leitura das linhas do file 
    file.close()                                 # Fecho do file
    nLines=0                                     # Contador para saber quantas linhas tem o file 
    dict_configFile={}                           # Dicionário para guardar as linhas lidas  
                                                 # TIPO DO DICT: (Nº da linha no ficheiro, Lista com os parâmetros existentes em cada linha do file)

    for line in lines:
        lista_Parametros=line.split(' ')         # Separação da linha em parâmetros (O caracter ' ' é o delimitador)
        dict_configFile[nLines]=lista_Parametros # Adicionar o par (key,value) ao dicionário
        nLines=nLines+1                          # Aumento do contador do número de linhas tratadas
    #Usado unicamente no debug do dicionário
    #for key in dict_configFile:
        #print(key)
        #print(dict_configFile[key])

main()