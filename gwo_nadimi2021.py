import random
import copy, math, sys
from ChaoticMaps import ChaoticMaps
import numpy as np

class IGWONadimi2021:

    def __init__(self, variableRanges, objFunction, popSize=100):
        self.variableRanges = variableRanges
        self.objFunction = objFunction
        self.popSize = popSize

    def createInitialPopulation(self, tupleData=None):
        population = []
        populationTemp = []

        for _ in range(self.popSize):
            randomVars = []
            
            for i in range(len(self.variableRanges)):
                randomVar = random.uniform(
                    0, 1) * (self.variableRanges[i][1] - self.variableRanges[i][0]) + self.variableRanges[i][0]
                
                while(randomVar < self.variableRanges[i][0] or randomVar > self.variableRanges[i][1]):
                    randomVar = random.uniform(0, 1) * (self.variableRanges[i][1] - self.variableRanges[i][0]) + self.variableRanges[i][0]
                
                randomVars.append(randomVar)
            
            objValue = self.objFunction.estimatingEffort(tupleData, randomVars)
            absError = abs(objValue-tupleData['actualEffort'])

            population.append({'objValue': objValue, 'variables': randomVars, 'absError': absError})

        a = 2.3
        R_k = 0.7

        for _ in range(self.popSize):
            randomVars = []
            R_k = ChaoticMaps(None).circle(R_k)

            for i in range(len(self.variableRanges)):
                randomVar = R_k * (self.variableRanges[i][1] - self.variableRanges[i][0]) + self.variableRanges[i][0]
                
                while(randomVar < self.variableRanges[i][0] or randomVar > self.variableRanges[i][1]):
                    randomVar = R_k * (self.variableRanges[i][1] - self.variableRanges[i][0]) + self.variableRanges[i][0]
                
                randomVars.append(randomVar)
            
            objValue = self.objFunction.estimatingEffort(tupleData, randomVars)
            absError = abs(objValue - tupleData['actualEffort'])

            populationTemp.append({'objValue': objValue, 'variables': randomVars, 'absError': absError})

        for i in range(self.popSize):
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

            objValue = self.objFunction.estimatingEffort(
                tupleData, newVars)

            population[idx] = {'objValue': objValue, 'variables': newVars, 'absError': abs(
                objValue - tupleData['actualEffort'])}

        return sorted(population, key=lambda x: x['absError'], reverse=False)
    
    def diversity(self, varValues):
        data = np.array(varValues)
        colsSum = np.sum(data, axis=0)
        allResults = []
        
        for i in range(self.popSize):
            varResults = []
            for j in range(len(self.variableRanges)):
                avg_j = colsSum[j] / self.popSize
                res = (varValues[i][j] - avg_j)**2
                varResults.append(res)
            allResults.append(math.sqrt(sum(varResults)))
        
        return sum(allResults) / self.popSize

    def runGWO(self, variableRanges, objFunction, tupleData, maxIter=20, popSize=100):
        bestWolf = {'objValue': None, 'absError': 10000}
        
        varValues = []
        population = self.createInitialPopulation(
            tupleData)
        for val in population:
            varValues.append(val['variables'])
        
        diversityRate = self.diversity(varValues)
        print(diversityRate)
        
        population = sorted(
            population, key=lambda x: x['absError'], reverse=False)
        
        for iter in range(maxIter):
            
            varValues = []
            
            # Initializing a, A, and C
            coefficient = 2
            a = coefficient - (coefficient * iter) / maxIter

            alphaA = (coefficient * a) * random.uniform(0, 1) - a
            betaA = (coefficient * a) * random.uniform(0, 1) - a
            deltaA = (coefficient * a) * random.uniform(0, 1) - a

            alphaC = coefficient * random.uniform(0, 1)
            betaC = coefficient * random.uniform(0, 1)
            deltaC = coefficient * random.uniform(0, 1)

            # 5. Encircling Prey
            alphaIndex = 0
            betaIndex = 1
            deltaIndex = 2

            alphaWolf = population[alphaIndex]
            alphaPopulation = self.preyHunting(
                population, alphaWolf['variables'], alphaC, alphaA, variableRanges, objFunction, tupleData)

            betaWolf = population[betaIndex]
            betaPopulation = self.preyHunting(
                population, betaWolf['variables'], betaC, betaA, variableRanges, objFunction, tupleData)

            deltaWolf = population[deltaIndex]
            deltaPopulation = self.preyHunting(
                population, deltaWolf['variables'], deltaC, deltaA, variableRanges, objFunction, tupleData)

            for i in range(popSize):
                positions = []

                for j in range(len(variableRanges)):

                    position = (alphaPopulation[i]['variables'][j] + betaPopulation[i]['variables']
                                [j] + deltaPopulation[i]['variables'][j]) / len(variableRanges)

                    positions.append(position)

                objValue = self.objFunction.estimatingEffort(
                    tupleData, positions)

                population[i] = {'objValue': objValue, 'variables': [
                    positions[0], positions[1]], 'absError': abs(objValue-tupleData['actualEffort'])}
                
                varValues.append([positions[0], positions[1]])

            if alphaWolf['absError'] < bestWolf['absError']:
                bestWolf = copy.deepcopy(alphaWolf)
            
            diversityRate = self.diversity(varValues)
            print(diversityRate)
            
            #print(bestWolf['absError'])
        #     convergences.append(bestWolf['absError'])
        
        # print(convergences)
        sys.exit()
        return bestWolf