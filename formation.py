import random
from bitarray import bitarray
class Formation:
    def __init__(self, defs, mid, fwd, st=None):
        self.GK = 1
        self.LB = 0
        self.CB = 0
        self.RB = 0
        self.RWB = 0
        self.CDM= 0
        self.LWB= 0
        self.CM= 0
        self.CAM= 0
        self.LW= 0
        self.RW= 0
        self.LM= 0
        self.RM  = 0
        self.ST= 0
        self.set_formation(defs, mid, fwd, st)
        self.PosDict= {
            'GK': self.GK,
            'LB': self.LB,
            'CB': self.CB,
            'RB': self.RB,
            'RWB': self.RWB,
            'CDM': self.CDM,
            'LWB': self.LWB,
            'CM': self.CM,
            'CAM': self.CAM,
            'RW': self.RW,
            'LW': self.LW,
            'LM': self.LM,
            'RM': self.RM,
            'ST': self.ST
        }
    def set_formation(self, defense, mid, fwd, st=None):
        if st is None:
            if defense == 4 and mid == 4 and fwd == 2:
                self.LB = 1
                self.CB = 2
                self.RB = 1
                self.LM = 1
                self.CM = 2
                self.RM = 1
                self.ST = 2
            elif defense == 4 and mid == 3 and fwd == 3:
                self.LB = 1
                self.CB = 2
                self.RB = 1
                self.CDM = 1
                self.CM = 2
                self.LW = 1
                self.RW = 1
                self.ST = 1        
        else:
            if defense == 4 and mid == 4 and st == 1 and fwd ==1:
                self.LB = 1
                self.CB = 2
                self.RB = 1
                self.CDM = 1
                self.CM = 2
                self.CAM = 1
                self.ST = 2
            elif defense == 4 and mid == 2 and st ==3 and fwd ==1:
                self.LB = 1
                self.CB = 2
                self.RB = 1
                self.CDM = 2
                self.LW = 1
                self.CAM = 1
                self.RW = 1
                self.ST = 1


    
          