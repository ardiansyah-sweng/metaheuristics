import random, copy, sys, math
import numpy as np

# GWO Origin
class GreyWolfOptimizer:

    def __init__(self, variableRanges, objFunction, popSize=100):
        self.variableRanges = variableRanges
        self.objFunction = objFunction
        self.popSize = popSize

    def createInitialPopulation(self, popSize, variableRanges, objFunction, tupleData=None):
        population = []; 
        
        for _ in range(popSize):
            randomVars = []
            for i in range(len(variableRanges)):
                randomVar = random.uniform(0,1) * (variableRanges[i][1] - variableRanges[i][0]) + variableRanges[i][0]
                
                while(randomVar < variableRanges[i][0] or randomVar > variableRanges[i][1]):
                    randomVar = random.uniform(0, 1) * (variableRanges[i][1] - variableRanges[i][0]) + variableRanges[i][0]
                
                randomVars.append(randomVar)

            objValue = objFunction.estimatingEffort(tupleData, randomVars)
            population.append({'objValue':objValue, 'variables':randomVars, 'absError':abs(objValue-tupleData['actualEffort'])})
        
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
            
            objValue = objFunction.estimatingEffort(tupleData, newVars)
            
            population[idx] = {'objValue': objValue, 'variables': newVars, 'absError': abs(objValue - tupleData['actualEffort'])}
        
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
        
        bestWolf = {'objValue':None, 'absError':10000000}
        
        varValues = []
        population = self.createInitialPopulation(popSize, variableRanges, objFunction, tupleData)
        
        for val in population:
            varValues.append(val['variables'])
        diversityRate = self.diversity(varValues)
        print(diversityRate)
        
        population = sorted(population, key=lambda x: x['absError'], reverse=False)        

        bestConvergences = []

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
            alphaIndex = 0; betaIndex = 1; deltaIndex = 2
            
            alphaWolf = population[alphaIndex]        
            alphaPopulation = self.preyHunting(population, alphaWolf['variables'], alphaC, alphaA, variableRanges, objFunction, tupleData)
            
            betaWolf = population[betaIndex]
            betaPopulation = self.preyHunting(population, betaWolf['variables'], betaC, betaA, variableRanges, objFunction, tupleData)
            
            deltaWolf = population[deltaIndex]
            deltaPopulation = self.preyHunting(
                population, deltaWolf['variables'], deltaC, deltaA, variableRanges, objFunction, tupleData)
                       
            for i in range(popSize):
                positions = []
                
                for j in range(len(variableRanges)):
                    
                    position = (alphaPopulation[i]['variables'][j] + betaPopulation[i]['variables'][j] + deltaPopulation[i]['variables'][j]) / len(variableRanges)
                    
                    positions.append(position)
                
                objValue = objFunction.estimatingEffort(tupleData, positions)
                
                population[i] = {'objValue': objValue, 'variables': [
                    positions[0], positions[1]], 'absError': abs(objValue-tupleData['actualEffort'])}
                
                varValues.append([positions[0], positions[1]])
            
            if alphaWolf['absError'] < bestWolf['absError']:
                bestWolf = copy.deepcopy(alphaWolf)
            
            diversityRate = self.diversity(varValues)
            print(diversityRate)
            
            # print(bestWolf['absError'])
            bestConvergences.append(bestWolf['absError'])
        # for data in bestConvergences:
        #     print(data)
        sys.exit()    
        return {
            'bestWolf':bestWolf,
            'bestConvergences':bestConvergences
        }