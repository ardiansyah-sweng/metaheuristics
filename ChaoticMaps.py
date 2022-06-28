import math

class ChaoticMaps:
    
    def __init__(self, iter):
        self.iter = iter
    
    def gauss(self, chaosValue):
        if (chaosValue == 0):
            chaosValue = 0.00000001
        return math.fmod(1 / chaosValue, 1)
    
    def bernoulli(self, chaosValue):
        if (chaosValue > 0 and chaosValue <= (1 - (1/2))):
            return chaosValue / (1 - (1/2))
        if (chaosValue > (1-(1/2)) and chaosValue < 1):
            return (chaosValue - (1 - (1/2))) / (1/2)
    
    def chebyshev(self, chaosValue):
        return math.cos(self.iter * math.cos(chaosValue**-1) )
    
    def circle(self, chaosValue):
        return math.fmod(chaosValue + 0.2 - (0.5 / (2 * math.pi)) * math.sin(2 * math.pi * chaosValue), 1)
    
    def logistic(self, chaosValue):
        return (4 * chaosValue) * (1 - chaosValue)
    
    def sine(self, chaosValue):
        return math.sin(math.pi * chaosValue)
    
    def singer(self, chaosValue):
        return 1.07 * ( (7.86 * chaosValue) - (23.31 * chaosValue**2) + (28.75 * chaosValue**3) - (13.302875 * chaosValue**4) )
    
    def sinu(self, chaosValue):
        return ( 2.3 * chaosValue**2 ) * math.sin(math.pi) * chaosValue