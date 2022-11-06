class pQuery:
    def __init__(self, msg, domain_server):
        self.msg = msg
        self.domain_server = domain_server

    # Exemplo de uma querie recebida : message_id flags 0 0 0 0 domain type
    def processQuery(self):
        query=str(self.msg)
        queryCheck=True
        lista_ParametrosQuery=query.split(' ')
        if (int(lista_ParametrosQuery[0])>1 and int(lista_ParametrosQuery[0])<65535):
            queryCheck=True
        else:
            return False
        lista_Flags=lista_ParametrosQuery[1].split('+')
        for it in lista_Flags:
            if (it=='R' or it=='Q' or it=='A'):
                queryCheck=True
            else:
                return False
        if(lista_ParametrosQuery[2]=='0' and lista_ParametrosQuery[3]=='0' and lista_ParametrosQuery[4]=='0' and lista_ParametrosQuery[5]=='0'):
                queryCheck=True
        else:
                return False
        if (lista_ParametrosQuery[6]==self.domain_server):
            queryCheck=True
        else:
            return False
        if (lista_ParametrosQuery[7]=='DEFAULT' or lista_ParametrosQuery[7]=='SOASP' or lista_ParametrosQuery[7]=='SOAADMIN' or\
            lista_ParametrosQuery[7]=='SOASERIAL' or  lista_ParametrosQuery[7]=='SOAREFRESH' or  lista_ParametrosQuery[7]=='SOARETRY' or\
            lista_ParametrosQuery[7]=='SOAEXPIRE' or lista_ParametrosQuery[7]=='NS' or lista_ParametrosQuery[7]=='A' or\
            lista_ParametrosQuery[7]=='CNAME' or lista_ParametrosQuery[7]=='MX' or lista_ParametrosQuery[7]=='PTR' ):
                        queryCheck=True
        else:
                return False
        
        return(lista_ParametrosQuery[0],queryCheck,lista_ParametrosQuery[7])