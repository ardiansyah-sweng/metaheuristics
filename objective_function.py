import sys

class CocomoEstimator:
    
    def __init__(self, cocomoCode):
        self.cocomoCode = cocomoCode

    def getEffortDriver(self, effortDriverName, effortDriverIndex):
        
        effortDrivers = {
                "prec": {"vl": 6.2, "l": 4.96, "n": 3.72, "h": 2.48, "vh": 1.24, "xh": 0},
                "flex": {"vl": 5.07, "l": 4.05, "n": 3.04, "h": 2.03, "vh": 1.01, "xh": 0},
                "resl": {"vl": 7.07, "l": 5.65, "n": 4.24, "h": 2.83, "vh": 1.41, "xh": 0},
                "team": {"vl": 5.48, "l": 4.38, "n": 3.29, "h": 2.19, "vh": 1.10, "xh": 0},
                "pmat": {"vl": 7.80, "l": 6.24, "n": 4.68, "h": 3.12, "vh": 1.56, "xh": 0},
                "rely": {"vl": 0.82, "l": 0.92, "n": 1.00, "h": 1.10, "vh": 1.26, "xh": 0},
                "data": {"vl": 0, "l": 0.90, "n": 1.00, "h": 1.14, "vh": 1.28, "xh": 0},
                "cplx": {"vl": 0.73, "l": 0.87, "n": 1.00, "h": 1.17, "vh": 1.34, "xh": 1.74},
                "ruse": {"vl": 0, "l": 0.95, "n": 1.00, "h": 1.07, "vh": 1.15, "xh": 1.24},
                "docu": {"vl": 0.81, "l": 0.91, "n": 1.00, "h": 1.11, "vh": 1.23, "xh": 0},
                "time": {"vl": 0, "l": 0, "n": 1.00, "h": 1.11, "vh": 1.29, "xh": 1.63},
                "stor": {"vl": 0, "l": 0, "n": 1.00, "h": 1.05, "vh": 1.17, "xh": 1.46},
                "pvol": {"vl": 0, "l": 0.87, "n": 1.00, "h": 1.15, "vh": 1.30, "xh": 0},
                "acap": {"vl": 1.42, "l": 1.19, "n": 1.00, "h": 0.85, "vh": 0.71, "xh": 0},
                "pcap": {"vl": 1.34, "l": 1.15, "n": 1.00, "h": 0.88, "vh": 0.76, "xh": 0},
                "pcon": {"vl": 1.29, "l": 1.12, "n": 1.00, "h": 0.90, "vh": 0.81, "xh": 0},
                "apex": {"vl": 1.22, "l": 1.10, "n": 1.00, "h": 0.88, "vh": 0.81, "xh": 0},
                "plex": {"vl": 1.19, "l": 1.09, "n": 1.00, "h": 0.91, "vh": 0.85, "xh": 0},
                "ltex": {"vl": 1.20, "l": 1.09, "n": 1.00, "h": 0.91, "vh": 0.84, "xh": 0},
                "tool": {"vl": 1.17, "l": 1.09, "n": 1.00, "h": 0.90, "vh": 0.78, "xh": 0},
                "site": {"vl": 1.22, "l": 1.09, "n": 1.00, "h": 0.93, "vh": 0.86, "xh": 0.80},
                "sced": {"vl": 1.43, "l": 1.14, "n": 1.00, "h": 1.00, "vh": 1.00, "xh": 0}
            }
        
        if effortDriverName in effortDrivers and effortDriverIndex in effortDrivers[effortDriverName]:
            return effortDrivers[effortDriverName][effortDriverIndex]

    def getScaleFactorValue(self, tupleData):
        scaleFactorValues = []
        scaleFactorsIndex = ['prec', 'flex', 'resl', 'team', 'pmat']
        
        for scaleName in tupleData:
            if scaleName in scaleFactorsIndex:
                scaleValue = self.getEffortDriver(scaleName, tupleData[scaleName])
                scaleFactorValues.append(scaleValue)
        
        return scaleFactorValues
    
    def getEffortMultiplierValue(self, tupledata):
        effortMultiplierValues = []
        
        effortMultiplierIndexes = ['rely', 'data', 'cplx', 'ruse', 'docu', 'time', 'stor','pvol', 'acap', 'pcap', 'pcon', 'apex', 'plex', 'ltex', 'tool', 'site', 'sced']
        
        for effortMultiplierName in tupledata:
            if effortMultiplierName in effortMultiplierIndexes:
                effortMultiplierValue = self.getEffortDriver(
                    effortMultiplierName, tupledata[effortMultiplierName])
                effortMultiplierValues.append(effortMultiplierValue)

        return effortMultiplierValues
        
    def estimatingEffort(self, tupleData, randomVars = [2.94, 0.91]):
        
        effortMultiplier = sum(self.getEffortMultiplierValue(tupleData))

        scaleFactor = sum(self.getScaleFactorValue(tupleData))
        klocExponent = randomVars[1] + 0.01 * scaleFactor       
        estimatedEffort = randomVars[0] * (tupleData['kloc']**klocExponent) * effortMultiplier
        
        return estimatedEffort