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
            results = UCWPSO.optimizing(dataPoints, self.popSize, seeds)
            optimizedAE = results[0]
            optimizedAEs.append(optimizedAE)
            optimizedPosition = results[1]
            optimizedPositions.append(optimizedPosition)
            sumAE += optimizedAE
            index += 1
        mae = sumAE / len(self.dataSet)
        return [mae, optimizedAEs, optimizedPositions]  

sumMAE = 0; sumSA = 0; sumES = 0
bestMAEs = []; bestPositions = []; bestOptimizedAEs = []; estimatedEfforts = []; estimateds = []; actualEfforts = []; runs = 30; fucpAEs = []; fucpEstimateds = []; runFUCPMAEs = []; fucpSAs = []; fucpESs = []; runFUCPAEs = []; runFUCPEstimateds = []

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
for i in range(runs):
    print('RUNS Ke- ', i)
    run = Executor(readSilhavy71(), popSize=30)
    finalResults = run.executing(dataSeeds[i])
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
       
    ## for FUCP
    for l in range(len(readSilhavy71())):
        #Define input range
        xMin1, xMax1 = 5, 7.49
        xMin2, xMax2 = 7.5, 12.49
        xMin3, xMax3 = 12.5, 15
        
        #Initial particles
        simple = random.uniform(xMin1, xMax1)
        average = random.uniform(xMin2, xMax2)
        complex = random.uniform(xMin3, xMax3)
        
        actualEffort = readSilhavy71()[l][-1]
        estimated = UCWPSO.estimatingUCP(readSilhavy71()[l], simple, average, complex)
        AE = abs(actualEffort - estimated)
        fucpEstimateds.append(estimated)
        fucpAEs.append(AE)
    runFUCPAEs.append(fucpAEs)
    runFUCPEstimateds.append(fucpEstimateds)
    fucpMAE = sum(fucpAEs) / len(fucpAEs)
    runFUCPMAEs.append(fucpMAE)
    fucpSAES = SAES(fucpMAE, actualEfforts)
    resFUCP = fucpSAES.calcSAES()
    fucpSAs.append(resFUCP[0])
    fucpESs.append(resFUCP[1])
    ## END FUCP
    
    
bestMAE = min(bestMAEs)
index = bestMAEs.index(bestMAE)
print('============')
print(' UCW + SPSO')
print('============')
print('Final MAE:', sumMAE/runs)
print('Final SA:', sumSA/runs)
print('Final ES:', sumES/runs)

# MBRE
balancer = Balancer.calcBalancer(bestOptimizedAEs[index], actualEfforts, estimatedEfforts[index])
print('MBRE: ', balancer[0])
print('MIBRE: ', balancer[1])

listToWrites = ['UCW+SPSO', 'MAE: ' + str(sumMAE/runs), 'SA: ' + str(sumSA/runs), 'ES: ' + str(sumES/runs), 'MBRE: ' + str(balancer[0]), 'MIBRE: ' + str(balancer[1]), ' ']
with open('results.txt', 'a') as f:
    for listToWrite in listToWrites:
        f.write(listToWrite)
        f.write('\n')
stringAEs = []
for x in bestMAEs:
    stringAEs.append(str(x))
with open('results.txt', 'a') as f:
    f.writelines('\n'.join(stringAEs))
print()

## for KARNER MODEL
karnerAEs = []; karnerMAes = []; karnerSAs = []; karnerESs = []; runKarnerActualEfforts = []; estimatedsKarner = []; runEstimatedsKarner = []; runKarnerAEs = []; karnerActualEfforts = []

for k in range(len(readSilhavy71())):   
    estimated = UCWPSO.estimatingUCP(readSilhavy71()[k], 5, 10, 15)
    karnerAEs.append(abs(actualEffort - estimated))
    estimatedsKarner.append(estimated)
    
MAEKarner = sum(karnerAEs) / len(readSilhavy71())
karnerSAES = SAES(MAEKarner, actualEfforts)
resKarner = karnerSAES.calcSAES()
# ## END KARNER MODEL

print('============')
print(' K A R N E R')
print('============')
print('Final MAE:', MAEKarner)
print('Final SA:', resKarner[0])
print('Final ES:', resKarner[1])
balancerKarner = Balancer.calcBalancer(karnerAEs, actualEfforts, estimatedsKarner)
print('MBRE: ', balancerKarner[0])
print('MIBRE: ', balancerKarner[1])
print()

listToWriteKarners = [' ', 'KARNER', 'MAE: ' + str(MAEKarner), 'SA: ' + str(resKarner[0]), 'ES: ' + str(resKarner[1]), 'MBRE: ' + str(balancerKarner[0]), 'MIBRE: ' + str(balancerKarner[1]), ' ']
with open('results.txt', 'a') as f:
    f.writelines('\n'.join(listToWriteKarners))

bestFUCPMAE = min(runFUCPMAEs)
indexFUCP = runFUCPMAEs.index(bestFUCPMAE)
print('============')
print(' F U C P    ')
print('============')
print('Final MAE:', sum(runFUCPMAEs) / runs)
print('Final SA:', sum(fucpSAs) / runs)
print('Final ES:', sum(fucpESs) / runs)
balancerFUCP = Balancer.calcBalancer(runFUCPAEs[indexFUCP], actualEfforts, runFUCPEstimateds[indexFUCP])
print('MBRE: ', balancerFUCP[0])
print('MIBRE: ', balancerFUCP[1])

listToWriteFUCPs = ['FUCP', 'MAE: ' + str(sum(runFUCPMAEs) / runs), 'SA: ' + str(sum(fucpSAs) / runs), 'ES: ' + str(sum(fucpESs) / runs), 'MBRE: ' + str(balancerFUCP[0]), 'MIBRE: ' + str(balancerFUCP[1]), ' ']
with open('results.txt', 'a') as f:
    f.writelines('\n'.join(listToWriteFUCPs))

stringFUCPAEs = []
for z in runFUCPMAEs:
    stringFUCPAEs.append(str(z))
with open('results.txt', 'a') as f:
    f.writelines('\n'.join(stringFUCPAEs))

print()