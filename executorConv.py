from DatasetReader import readSilhavy71
from numpy.random import rand
import sys
from UCWPSO import UCWPSO
from CPSO import CPSO
from performevaluation.SAES import SAES
from performevaluation.Balancer import Balancer
import random
from Estimator import UseCasePoints

class Executor:
    def __init__(self, dataSet, popSize):
        self.dataSet = dataSet
        self.popSize = popSize
        
    def executing(self, seeds):
        sumAE = 0; optimizedAEs = []; optimizedPositions = []; index = 0
        for dataPoints in self.dataSet:
            results = CPSO.optimizing(dataPoints, self.popSize, seeds)
            optimizedAE = results[0]
            optimizedAEs.append(optimizedAE)
            optimizedPosition = results[1]
            optimizedPositions.append(optimizedPosition)
            sumAE += optimizedAE
            index += 1
        mae = sumAE / len(self.dataSet)
        return [mae, optimizedAEs, optimizedPositions]  

sumMAE = 0; sumSA = 0; sumES = 0
bestMAEs = []; bestPositions = []; bestOptimizedAEs = []; estimatedEfforts = []; estimateds = []; actualEfforts = []; runs = 5; fucpAEs = []; fucpEstimateds = []; runFUCPMAEs = []; fucpSAs = []; fucpESs = []; runFUCPAEs = []; runFUCPEstimateds = []

def getSeeds():
    fileNames = [
        'ucp\seeds0.txt', 'ucp\seeds1.txt', 'ucp\seeds2.txt', 'ucp\seeds3.txt', 'ucp\seeds4.txt', 'ucp\seeds5.txt', 'ucp\seeds6.txt', 'ucp\seeds7.txt', 'ucp\seeds8.txt', 'ucp\seeds9.txt', 'ucp\seeds10.txt', 'ucp\seeds11.txt', 'ucp\seeds12.txt', 'ucp\seeds13.txt', 'ucp\seeds14.txt', 'ucp\seeds15.txt', 'ucp\seeds16.txt', 'ucp\seeds17.txt','ucp\seeds18.txt','ucp\seeds19.txt','ucp\seeds20.txt','ucp\seeds21.txt','ucp\seeds22.txt','ucp\seeds23.txt','ucp\seeds24.txt','ucp\seeds25.txt','ucp\seeds26.txt','ucp\seeds27.txt','ucp\seeds28.txt','ucp\seeds29.txt',
    ]; dataSets = []
    for fileName in fileNames:
        with open(fileName, "r") as myfile:
            datasetInString = myfile.read().replace("\n",",")
            datasetInList = datasetInString.split(",")    
            oneDataPoints, dataSet = [], []
            startIndex = 0
            for i in range(30):   ## TODO find out why i,j unused?
                for j in range(3):
                    oneDataPoints.append(float(datasetInList[startIndex]))
                    startIndex += 1
                dataSet.append(oneDataPoints)
                oneDataPoints = []
            startIndex = 0
        dataSets.append(dataSet)
        dataSet = []
    return dataSets

print()

dataSeeds = getSeeds()
popSize = 26

for x in range(15):
    for i in range(runs):
        print('RUNS Ke- ', i)
        run = Executor(readSilhavy71(), popSize)
        finalResults = run.executing(dataSeeds[i][0:popSize])
        MAEPi = finalResults[0]
        bestMAEs.append(MAEPi)
        bestOptimizedAEs.append(finalResults[1])
        bestPositions.append(finalResults[2])
        
        for j in range(len(readSilhavy71())):
            actualEffort = readSilhavy71()[j][-1]
            actualEfforts.append(actualEffort)
            estimated = UseCasePoints.estimatingUCP(readSilhavy71()[j], finalResults[2][j][0], finalResults[2][j][1], finalResults[2][j][2])
            estimateds.append(estimated)
        estimatedEfforts.append(estimateds)
        estimateds = []

        saes = SAES(MAEPi, actualEfforts)
        res = saes.calcSAES()

        SA = res[0]
        ES = res[1]
        sumMAE += MAEPi
        sumSA += SA
        sumES += ES
           
    bestMAE = min(bestMAEs)
    index = bestMAEs.index(bestMAE)
    finalMAE = sumMAE/runs
    print('popSize: ', popSize, ' MAE: ', finalMAE)

    listToWrites = ['UCW+CPSO Gauss', 'MAE: ' + str(finalMAE), 'popSize: ' + str(popSize)]
    with open('results.txt', 'a') as f:
        for listToWrite in listToWrites:
            f.write(listToWrite)
            f.write('\n')
    sumMAE = 0; listToWrites = []; finalMAE = []
    popSize += 2