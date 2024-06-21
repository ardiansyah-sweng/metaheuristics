import random
import sys, copy, math
from helper import MetaheuristicHelper as metaHelper
from testfunctions.multimodal import MultimodalFunctionsFactory

class FireflyOptimizer:
    def __init__(self, optimizerParameters, testFunctionParameters, testFunctionID):
        self.maxIter = optimizerParameters['maxIter']
        self.populationSize = optimizerParameters['populationSize']
        self.FAParameters = optimizerParameters
        self.testFunctionParameters = testFunctionParameters
        self.testFunctionID = testFunctionID
        
    def createNewFF(self, positions):
        objectiveValue = MultimodalFunctionsFactory.initializingMultimodalFunctions(self.testFunctionID, positions)
        return {
                'fitnessValue': metaHelper(
                    None,None,None,None,None
                    ).fitnessFunction(objectiveValue),
                'objectiveValue':objectiveValue, 
                'positions':positions
        }
        
    def moveDimFFtoBrightFF(self, brightFF, dimFF):
        for i in range(self.testFunctionParameters['dimension']):
            distance = math.sqrt((brightFF['positions'][i] - dimFF['positions'][i])**2)
                
            attractiveness = self.FAParameters['beta'] * math.exp(-self.FAParameters['gamma'] * (distance**2))
                
            randomEpsilon = random.randint(int(self.FAParameters['minEpsilon'] * 100), int(self.FAParameters['maxEpsilon'] * 100)) / 100
                
            dimFF['positions'][i] = dimFF['positions'][i] + attractiveness * (brightFF['positions'][i] - dimFF['positions'][i]) + self.FAParameters['alpha'] * randomEpsilon
                
            if dimFF['positions'][i] < self.testFunctionParameters['ranges'][0]:
                    dimFF['positions'][i] = self.testFunctionParameters['ranges'][0]
            if dimFF['positions'][i] > self.testFunctionParameters['ranges'][1]:
                    dimFF['positions'][i] = self.testFunctionParameters['ranges'][1]
                
        return self.createNewFF(dimFF['positions'])

    def runFirefly(self, population):
        bestFF = {
            'positions':None,
            'objectiveValue':None,
            'fitnessValue': 0
        }

        bestID = 0; bestConvergences = []
        for _ in range(self.maxIter):
            for i in range(len(population)):
                for j in range(len(population)):
                    if population[j]['fitnessValue'] > population[i]['fitnessValue']:
                        population[i] = self.moveDimFFtoBrightFF(population[j], population[i])
            population = sorted(population, key=lambda x: x['fitnessValue'], reverse=True)
            bestConvergences.append(bestFF['fitnessValue'])
            if population[bestID]['fitnessValue'] > bestFF['fitnessValue']:
                bestFF = copy.deepcopy(population[bestID])
        return {
            'bestSolution':bestFF, 
            'bestConvergence':bestConvergences
        }