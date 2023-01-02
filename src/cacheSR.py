from entryCache import *
class cache:

    def __init__(self):
        self.cache=dict()
        self.numeroEntradas=0

    def addEntry(self,entry):
        entry.setIndex(self.numeroEntradas)
        self.cache[self.numeroEntradas]=entry
        self.numeroEntradas=self.numeroEntradas+1


        