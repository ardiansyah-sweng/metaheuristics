import numpy as np
from DatasetReader import readSilhavy71
import sys

# Standardized Accuray and Effect Size
class SAES:
    sumSA = 0.0
    recurrSumAE = 0.0

    def __init__(self, MAEPi, actualEfforts, numRuns = 1000):
        self.MAEPi = MAEPi
        self.actualEfforts = actualEfforts
        self.numRuns = numRuns

    def getRandomGuessing(self):
        selectedEstimateds = []
        numActualEffort = len(self.actualEfforts)
        for i in range(numActualEffort):
            actualEffortsAfterDelete = np.delete(self.actualEfforts, i)
            selectedEstimated = np.random.choice(actualEffortsAfterDelete, 1)
            selectedEstimateds.append(selectedEstimated[0])
        return selectedEstimateds    
    
    def calcSAES(self):
        P0 = []
        numData = len(self.getRandomGuessing())

        for i in range(self.numRuns):
            estimateds = self.getRandomGuessing()
            for j in range(numData):
                ae = abs(estimateds[j] - self.actualEfforts[j])           
                self.recurrSumAE += ae
            mae = self.recurrSumAE / numData
            self.sumSA += mae
            P0.append(mae)
            mae = 0.0
        MAEP0 = self.sumSA / self.numRuns
        SA = (1 - (self.MAEPi / MAEP0)) * 100
        ES = abs(self.MAEPi - MAEP0) / np.std(P0)
        return [SA, ES]

## Temporary Method to prepare actual efforts
# actualEfforts = []
# for dataPoints in readSilhavy71():
#     actualEfforts.append(dataPoints[-1])

# SA = StandardizedAccuracy(1.208290704, actualEfforts)
# print(SA.calcSA())