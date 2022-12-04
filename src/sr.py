# Started in: 4/12/2022
# Changed by: Gonçalo Braga, João Gonçalves and Miguel Senra
# Finished in: 2/1/23


from cacheSR import cache
from entryCache import entry
class sr:
    
    def runSR():
        c=cache()
        e1=entry("campeoesUM.lei","MX","mx1.campeoesUM.lei","15","10","SP","5s","0","Valid")
        e2=entry("campeoesUM.lei","MX","mx2.campeoesUM.lei","17","10","SP","5s","0","Valid")
        e3=entry("campeoesUM.lei","MX","mx3.campeoesUM.lei","18","10","SP","2s","0","Valid")
        e4=entry("campeoesUM.lei","MX","mx4.campeoesUM.lei","18","10","SP","1s","0","Valid")
        c.addEntry(e1)
        c.addEntry(e2)
        c.addEntry(e3)
        c.addEntry(e4)

        for i in c.cache.keys():
            print(c.cache[i].stringEntry())





        


def main():
    sr.runSR()

if __name__ == "__main__":
    main()