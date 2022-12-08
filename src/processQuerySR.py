# Started in: 31/09/2022
# Changed by: Gonçalo Braga, João Gonçalves and Miguel Senra
# Finished in: 23/11/2022

class pQuerySR:
    def __init__(self, msg):
        self.msg = msg
        self.message_id=""
        self.typeValue=""
    def processQuery(self): # 0: A querie recebida está correta
                            # 1: A querie recebida está errada
            query=str(self.msg)
            queryCheck=0
            lista_ParametrosQuery=query.split(' ')
            if (int(lista_ParametrosQuery[0])>1 and int(lista_ParametrosQuery[0])<65535):
                queryCheck=0
            else:
                return 1
            lista_Flags=lista_ParametrosQuery[1].split('+')
            for it in lista_Flags:
                if (it=='R' or it=='Q' or it=='A'):
                    queryCheck=0
                else:
                    return 1
            if(lista_ParametrosQuery[2]=='0' and lista_ParametrosQuery[3]=='0' and lista_ParametrosQuery[4]=='0' and lista_ParametrosQuery[5]=='0'):
                    queryCheck=0
            else:
                    return 1
            if (lista_ParametrosQuery[7]=='DEFAULT' or lista_ParametrosQuery[7]=='SOASP' or lista_ParametrosQuery[7]=='SOAADMIN' or\
                lista_ParametrosQuery[7]=='SOASERIAL' or  lista_ParametrosQuery[7]=='SOAREFRESH' or  lista_ParametrosQuery[7]=='SOARETRY' or\
                lista_ParametrosQuery[7]=='SOAEXPIRE' or lista_ParametrosQuery[7]=='NS' or lista_ParametrosQuery[7]=='A' or\
                lista_ParametrosQuery[7]=='CNAME' or lista_ParametrosQuery[7]=='MX' or lista_ParametrosQuery[7]=='PTR' ):
                            queryCheck=0
            else:
                    return 1
            self.message_id=lista_ParametrosQuery[0]
            self.typeValue=lista_ParametrosQuery[7]   

            return queryCheck,lista_ParametrosQuery[6]