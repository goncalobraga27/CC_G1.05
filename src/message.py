
class message:

    def __init__(self,messageID,flags,responseCode,numberOfValues,numberOfAuthorities,numberOfExtraValues,nameDomain,typeOfValue,responseValues,authoritiesValues,extraValues):
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

        match self.flags:
            case "Q":
                flags = 0
            case "R":
                flags = 1
            case "A":
                flags = 2
            case "Q+R":
                flags = 3
            case "AR":
                flags = 4

        flags = bin(flags)
        flags = flags[2:]

        byte = int(flags,2)
        byte = byte.to_bytes(1,"big",signed=False)

        return byte

    def encodeResponseCode(self):
        resp = -1

        match self.responseCode:
            case "0":
                resp = 0
            case "1":
                resp = 1
            case "2":
                resp = 2
            case "3":
                resp = 3

        resp = bin(resp)
        resp = resp[2:]

        byte = int(resp,2)
        byte = byte.to_bytes(1,"big",signed=False)

        return byte


    def encodeTypeOfValue(self):
        resp = -1
        # Query Type
        # SOASP - 0, SOAADMIN - 1, SOASERIAL - 2, SOAREFRESH - 3, SOARETRY -4, SOAEXPIRE - 5, NS - 6, A - 7,
        # CNAME - 8, MX - 9, PTR - 10
        match self.typeOfValue:
            case "SOASP":
                resp = 0
            case "SOAADMIN":
                resp = 1
            case "SOASERIAL":
                resp = 2
            case "SOAREFRESH":
                resp = 3
            case "SOARETRY":
                resp = 4
            case "SOAEXPIRE":
                resp = 5
            case "NS":
                resp = 6
            case "A":
                resp = 7
            case "CNAME":
                resp = 8
            case "MX":
                resp = 9
            case "PTR":
                reap = 10

        resp = bin(resp)
        resp = resp[2:]

        byte = int(resp, 2)
        byte = byte.to_bytes(1, "big", signed=False)

        return byte


    def serialize(self):
        bytes = b''

        # MessageID - 2 bytes
        msg_id = self.messageID.to_bytes(2, "big", signed=False)
        bytes += msg_id

        #flags - 3 bits
        flags = self.encodeFlags()
        bytes += flags

        #Response Code - 2 bits
        rCode = self.encodeResponseCode()
        bytes += rCode

        #Number of Values - 1 byte
        nOfValues = self.numberOfValues.to_bytes(1,"big", signed=False)
        bytes+=nOfValues

        #Number of Authorities - 1 byte
        nOfAuthorities = self.numberOfAuthorities.to_bytes(1,"big", signed=False)
        bytes += nOfAuthorities

        #Number of Extra Values - 1 byte
        nOfExtraValues = self.numberOfExtraValues.to_bytes(1, "big", signed=False)
        bytes += nOfExtraValues

        #name - UTF-8
        len_domain = len(self.nameDomain).to_bytes(1, "big", signed=False)
        domain = self.nameDomain.encode('utf-8')
        bytes += len_domain + domain

        #typeOfValue - 4 bits
        rtypeOfValue = self.encodeTypeOfValue()
        bytes += rtypeOfValue

        #Response Values - UTF-8
        len_RValues = len(self.responseValues).to_bytes(1, "big", signed=False)
        responseValues = self.responseValues.encode('utf-8')
        bytes += len_RValues + responseValues

        #Authorities Values - UTF-8
        len_AValues = len(self.authoritiesValues).to_bytes(1, "big", signed=False)
        authoritiesValues = self.authoritiesValues.encode('utf-8')
        bytes += len_AValues + authoritiesValues

        #Extra Values - UTF-8
        len_EValues = len(self.extraValues).to_bytes(1,"big", signed=False)
        extraValues = self.extraValues.encode('utf-8')
        bytes += len_EValues + extraValues

        return bytes

