import sys
#conflict test1
 
########################################################################
class CarClass:
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, color, make, model, year):
        """Constructor"""
        self.color = color
        self.make = make
        self.model = model
        self.year = year
        print "ok"
 
        if "Windows" in platform.platform():
            pass
        self.weight = self.getWeight(1, 2, 3)
 
    #----------------------------------------------------------------------
    def getWeight(this):
        """"""
        return "2000 lbs"
