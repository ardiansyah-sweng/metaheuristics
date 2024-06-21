import random, copy, sys, math
from dataclasses import dataclass

# Z. Yang, “Competing leaders grey wolf optimizer and its application for training multi-layer perceptron classifier,” Expert Syst. Appl., vol. 239, no. October 2023, p. 122349, 2024, doi: 10.1016/j.eswa.2023.122349.
    
class CGreyWolfOptimizerYang2023:

    def __init__(self, variableRanges, objFunction, popSize=100):
        self.variableRanges = variableRanges
        self.objFunction = objFunction
        self.popSize = popSize
    
    def createInitialPopulation(self, popSize, variableRanges, objFunction, tupleData=None):
        population = []; populationTemp = []
        
        for _ in range(popSize):
            randomVars = []
            for i in range(len(variableRanges)):
                randomVar = random.gauss(0,1) * (variableRanges[i][1] - variableRanges[i][0]) + variableRanges[i][0]
                
                while(randomVar < variableRanges[i][0] or randomVar > variableRanges[i][1]):
                    randomVar = random.gauss(0, 1) * (variableRanges[i][1] - variableRanges[i][0]) + variableRanges[i][0]

                randomVars.append(randomVar)
            
            objValue = self.objFunction.estimatingEffort(tupleData, randomVars)
            absError = abs(objValue-tupleData['actualEffort'])
            
            population.append({'objValue':objValue, 'variables':randomVars, 'absError':absError})
        
        a = 2.3
        R_k = 0.7
        for _ in range(popSize):
            randomVars = []
            R_k = (a * (R_k**2)) * math.sin(math.pi * R_k)
            
            for i in range(len(variableRanges)):
                randomVar = R_k * (variableRanges[i][1] - variableRanges[i][0]) + variableRanges[i][0]

                while(randomVar < variableRanges[i][0] or randomVar > variableRanges[i][1]):
                    randomVar = R_k * (variableRanges[i][1] - variableRanges[i][0]) + variableRanges[i][0]                
                
                randomVars.append(randomVar)
                        
            objValue = self.objFunction.estimatingEffort(tupleData, randomVars)
            absError = abs(objValue - tupleData['actualEffort'])
            
            populationTemp.append({'objValue': objValue, 'variables': randomVars, 'absError': absError})
        
        for i in range(popSize):
            if population[i]['absError'] > populationTemp[i]['absError']:
                population[i] = populationTemp[i]
        
        return population
    
    def preyHunting(self, population, wolfType, C, A, variableRanges, objFunction, tupleData):
        
        for idx, wolf in enumerate(population):
            newVars = []
            
            for i in range(len(wolfType)):

                D = abs(C * wolfType[i] - wolf['variables'][i])
                newVar = wolfType[i] - A * D
                
                if newVar < variableRanges[i][0]:
                    newVar = variableRanges[i][0]
                if newVar > variableRanges[i][1]:
                    newVar = variableRanges[i][1]
                
                newVars.append(newVar)
            
            objValue = self.objFunction.estimatingEffort(tupleData, newVars)
            
            population[idx] = {'objValue': objValue, 'variables': newVars, 'absError': abs(objValue - tupleData['actualEffort'])}
        
        return sorted(population, key=lambda x: x['absError'], reverse=False)
    
    def runGWO(self, variableRanges, objFunction, tupleData, maxIter=20, popSize=100):
        
        bestWolf = {'objValue':None, 'absError':10000} # for minimum problem
        
        population = self.createInitialPopulation(popSize, variableRanges, objFunction, tupleData)
        population = sorted(population, key=lambda x: x['absError'], reverse=False)

        Mmin = 3
        MXupper = (Mmin + 1) * 10
        MXlower = Mmin
        
        bestConvergences = []
        
        if len(variableRanges) <= (4 * popSize):
            Mmax = round((len(variableRanges)/popSize) * (MXupper -  MXlower) + MXlower )
        if len(variableRanges) > (4 * popSize):
            Mmax = MXupper
        
        leadersA = []; leadersC = []
        
        for iter in range(maxIter):
            
            if iter < 3 / (4 * maxIter):
                M = round(Mmax - iter * ( (4 * (Mmax - Mmin)) / 3 * maxIter))
            if iter >= 3 / (4 * maxIter):
                M = Mmin
            
            updatedsPopulation = []
            
            # Initializing a, A, and C
            coefficient = 2
            a = coefficient - (coefficient * iter) / maxIter
            
            for _ in range(M):
                leadersA.append((coefficient * a) * random.uniform(0, 1) - a)
                leadersC.append(coefficient * random.uniform(0, 1))
                   
            # 5. Encircling Prey
            for i in range(M):
                
                updatedPopulation = self.preyHunting(population, population[i]['variables'], leadersC[i], leadersA[i], variableRanges, objFunction, tupleData)
                
                updatedsPopulation.append(updatedPopulation)
                
            for i in range(popSize):
                positions = []
                
                for j in range(len(variableRanges)):
                    
                    position = 0
                    for k in range(M):
                        position = position + updatedsPopulation[k][i]['variables'][j]
                    
                    meanPosition = position / M
                     
                    if meanPosition < variableRanges[j][0]:
                        meanPosition = variableRanges[j][0]
                    if meanPosition > variableRanges[j][1]:
                        meanPosition = variableRanges[j][1]
                    
                    positions.append(meanPosition)
                
                objValue = self.objFunction.estimatingEffort(tupleData, positions)
                
                population[i] = {'objValue': objValue, 'variables': [
                    positions[0], positions[1]], 'absError': abs(objValue-tupleData['actualEffort'])}
            
            sorted(population, key=lambda x: x['absError'], reverse=False)
            
            if population[0]['absError'] < bestWolf['absError']:
                bestWolf = copy.deepcopy(population[0])
            
            bestConvergences.append(bestWolf['absError'])
        
        # for data in bestConvergences:
        #     print(data)

        return bestWolf
