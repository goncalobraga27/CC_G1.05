class MessageDNS:

    def __init__(self, messageID=0, flags="", responseCode=0, numberOfValues=0, numberOfAuthorities=0, numberOfExtraValues=0,
                 nameDomain="", typeOfValue="", responseValues="", authoritiesValues="", extraValues=""):
        self.messageID = messageID
        self.flags = flags
        self.responseCode = responseCode
        self.numberOfValues = numberOfValues
        self.numberOfAuthorities = numberOfAuthorities
        self.numberOfExtraValues = numberOfExtraValues
        self.nameDomain = nameDomain
        self.typeOfValue = typeOfValue
        self.responseValues = responseValues
        self.authoritiesValues = authoritiesValues
        self.extraValues = extraValues


    def encodeFlags(self):
        flags = -1
        
        if self.flags == "Q":
            flags = 0
        if self.flags == "R":
            flags = 1
        if self.flags == "A":
            flags = 2
        if self.flags == "Q+R":
            flags = 3
        if self.flags == "R+A":
            flags = 4

        byte = flags.to_bytes(1, "big", signed=False)

        return byte
    

    def decodeFlags(self,num):
        if num == 0:
            self.flags ="Q"
        elif num == 1:
            self.flags ="R"
        elif num == 2:
            self.flags = "A"
        elif num == 3:
            self.flags = "Q+R"
        elif num == 4:
            self.flags = "R+A"
            

    def encodeResponseCode(self):
        resp= int(self.responseCode)
        if resp not in range(0,4):
            resp=0

        byte = resp.to_bytes(1, "big", signed=False)

        return byte
    

    def decodeResponseCode(self,num):
        self.responseCode = str(num)
        
        
    def encodeTypeOfValue(self):
        resp = -1
        # Query Type
        # SOASP - 0, SOAADMIN - 1, SOASERIAL - 2, SOAREFRESH - 3, SOARETRY -4, SOAEXPIRE - 5, NS - 6, A - 7,
        # CNAME - 8, MX - 9, PTR - 10
        if self.typeOfValue == "SOASP":
            resp = 0
        elif self.typeOfValue == "SOAADMIN":
            resp = 1
        elif self.typeOfValue == "SOASERIAL":
            resp = 2
        elif self.typeOfValue == "SOAREFRESH":
            resp = 3
        elif self.typeOfValue == "SOARETRY":
            resp = 4
        elif self.typeOfValue == "SOAEXPIRE":
            resp = 5
        elif self.typeOfValue == "NS":
            resp = 6
        elif self.typeOfValue == "A":
            resp = 7
        elif self.typeOfValue == "CNAME":
            resp = 8
        elif self.typeOfValue == "MX":
            resp = 9
        elif self.typeOfValue == "PTR":
            resp = 10

        byte = resp.to_bytes(1, "big", signed=False)

        return byte
    

    def decodeTypeOfValue(self,num):
        # Query Type
        # SOASP - 0, SOAADMIN - 1, SOASERIAL - 2, SOAREFRESH - 3, SOARETRY -4, SOAEXPIRE - 5, NS - 6, A - 7,
        # CNAME - 8, MX - 9, PTR - 10
        if num==0:
            self.typeOfValue = "SOASP"
        elif num==1:
            self.typeOfValue == "SOAADMIN"
        elif  num==2:
            self.typeOfValue = "SOASERIAL"
        elif num==3:
            self.typeOfValue ="SOAREFRESH"
        elif num==4:
            self.typeOfValue = "SOARETRY"
        elif num==5:
            self.typeOfValue ="SOAEXPIRE"
        elif num==6:
            self.typeOfValue ="NS"
        elif num==7:
            self.typeOfValue = "A"
        elif num==8:
            self.typeOfValue = "CNAME"
        elif num==9:
            self.typeOfValue = "MX"
        elif num==10:
            self.typeOfValue = "PTR"
            
            
    def serialize(self):
        bytes = b''

        # MessageID - 2 bytes
        msg_id = (self.messageID).to_bytes(2, "big", signed=False)
        bytes += msg_id

        # flags - 3 bits
        flags = self.encodeFlags()
        bytes += flags

        # Response Code - 2 bits
        rCode = self.encodeResponseCode()
        bytes += rCode


        ExistRV = self.numberOfValues!=0
        b1 = ExistRV.to_bytes(1,"big")
        bytes+=b1

        # Number of Values - 1 byte
        if ExistRV:
            nOfValues = (self.numberOfValues).to_bytes(1, "big", signed=False)
            bytes += nOfValues
            

        ExistAV = self.numberOfAuthorities!=0
        b1= ExistAV.to_bytes(1, "big")
        bytes+=b1

        # Number of Authorities - 1 byte
        if ExistAV:
            nOfAuthorities = (self.numberOfAuthorities).to_bytes(1, "big", signed=False)
            bytes += nOfAuthorities
        

        ExistEV = self.numberOfExtraValues!=0
        b1= ExistEV.to_bytes(1, "big")
        bytes+=b1

        # Number of Extra Values - 1 byte
        if ExistEV:
            nOfExtraValues = (self.numberOfExtraValues).to_bytes(1, "big", signed=False)
            bytes += nOfExtraValues

        # name - UTF-8
        len_domain = len(self.nameDomain).to_bytes(1, "big", signed=False)
        domain = self.nameDomain.encode('utf-8')
        bytes += len_domain + domain
    
        # typeOfValue - 4 bits
        rtypeOfValue = self.encodeTypeOfValue()
        bytes += rtypeOfValue
        

        # Response Values - UTF-8

        if ExistRV:
            tam = len (self.responseValues).to_bytes(4,"big",signed=False)
            byte=self.responseValues.encode('utf-8')
            bytes += tam + byte

        # Authorities Values - UTF-8
        if ExistAV:
            tam = len(self.authoritiesValues).to_bytes(4, "big", signed=False)
            byte = self.authoritiesValues.encode('utf-8')
            bytes += tam + byte
            
        # Extra Values - UTF-8
        if ExistEV:
            tam = len(self.extraValues).to_bytes(4, "big", signed=False)
            byte = self.extraValues.encode('utf-8')
            bytes += tam + byte

        return bytes
    
    def take_bytes(self,bytes, number):
        ret = bytes[:number]
        bytes = bytes[number:]

        return ret, bytes
    
    

    def deserialize(self, bytes):

        #message-ID
        res, bytes = self.take_bytes(bytes, 2)
        self.messageID = int.from_bytes(res, "big",signed=False)

        #Flags
        res, bytes = self.take_bytes(bytes, 1)
        num = int.from_bytes(res, "big", signed=False)
        self.decodeFlags(num)

        #ResponseCode
        res, bytes = self.take_bytes(bytes, 1)
        self.responseCode = int.from_bytes(res, "big", signed=False)

        #Verify if exists Response Value
        res, bytes = self.take_bytes(bytes, 1)
        ExistRV = bool.from_bytes(res, "big")

        #Response Values
        if ExistRV:
            res, bytes = self.take_bytes(bytes, 1)
            self.numberOfValues = int.from_bytes(res, "big", signed=False)

        #Verify if exists Authority Values
        res, bytes = self.take_bytes(bytes, 1)
        ExistAV = bool.from_bytes(res, "big")

        #Authority Values
        if ExistAV:
            res, bytes = self.take_bytes(bytes, 1)
            self.authoritiesValues = int.from_bytes(res, "big", signed=False)

        #Verify if exists Extra Values
        res, bytes = self.take_bytes(bytes, 1)
        ExistEV = bool.from_bytes(res, "big")

        #Extra Values
        if ExistEV:
            res, bytes = self.take_bytes(bytes, 1)
            self.extraValues = int.from_bytes(res, "big", signed=False)

        #Verify the length of the domain
        res, bytes = self.take_bytes(bytes, 1)
        tam=int.from_bytes(res, "big", signed=False)

        #Domain
        res, bytes = self.take_bytes(bytes, tam)
        self.nameDomain = res.decode("utf-8")

        #Type of Value
        res, bytes = self.take_bytes(bytes, 1)
        val = int.from_bytes(res, "big", signed=False)
        self.decodeTypeOfValue(val)

        #Verify if exists Response Values, and if so decode UTF-8
        if ExistRV:
            res, bytes = self.take_bytes(bytes, 4)
            tam = int.from_bytes(res, "big", signed=False)
            res, bytes = self.take_bytes(bytes, tam)
            self.responseValues = res.decode('utf-8')

        #Verify if exists Authorities Values, and if so decode UTF-8
        if ExistAV:
            res, bytes = self.take_bytes(bytes, 4)
            tam = int.from_bytes(res, "big", signed=False)
            res, bytes = self.take_bytes(bytes, tam)
            self.authoritiesValues = res.decode('utf-8')
            
        #Verify if exists Extra Values, and if so decode UTF-8
        if ExistEV:
            res, bytes = self.take_bytes(bytes, 4)
            tam = int.from_bytes(res, "big", signed=False)
            res, bytes = self.take_bytes(bytes, tam)
            self.extraValues = res.decode('utf-8')
            
            
        return str(self.messageID) + " " + self.flags + " " + str(self.responseCode) + " " + str(self.numberOfValues) + " " + str(self.numberOfAuthorities) + " " + str(self.numberOfExtraValues) + " " + self.nameDomain + " " + self.typeOfValue + " " + self.responseValues + " " + self.authoritiesValues + " " + self.extraValues