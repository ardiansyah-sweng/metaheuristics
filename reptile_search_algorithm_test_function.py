import random
import sys
import copy
from testfunctions.multimodal import MultimodalFunctionsFactory
import numpy as np
from helper import MetaheuristicHelper

class EvolutionarySense:
    def __init__(self, maxIter) -> None:
        self.maxIter = maxIter
    
    def ES(self):
        return random.randint(-1,1) * (1 - (1 / self.maxIter))

class WalkingMovementStrategy:
    def __init__(self, beta, maxIter):
        self.beta = beta
        self.maxIter = maxIter
    
    def highWalking(self, bestReptile, etaPositions, reducedPositions):
        rets = []; results = []
        for i in range(len(etaPositions)):
            for j in range(len(etaPositions[i])):
                result = bestReptile['positions'][j] * etaPositions[i][j] * self.beta - reducedPositions[i][j] * random.uniform(0,1)
                results.append(result)
            rets.append(results)
            results = []
        return rets
    
    def bellyWalking(self, bestReptile, population):
        rets = []; results = []
        for _ in range(len(population)):
            r1 = random.randint(0, len(population)-1)
            x_r1j = population[r1]
            for j in range(len(x_r1j['positions'])):
                result = bestReptile['positions'][j] * x_r1j['positions'][j] * EvolutionarySense(self.maxIter).ES()
                results.append(result)
            rets.append(results)
            results = []
        return rets
    
    def huntingCoordination(self, bestReptile, percentageDiff):
        rets = []; results = []
        for i in range(len(percentageDiff)):
            for j in range(len(bestReptile['positions'])):
                result = bestReptile['positions'][j] * percentageDiff[i][j] * random.uniform(0,1)
                results.append(result)
            rets.append(results)
            results = []
        return rets
    
    def huntingCooperation(self, bestReptile, etaPositions, reducedPositions, smallNumber):
        rets = []; results = []
        for i in range(len(etaPositions)):
            for j in range(len(bestReptile['positions'])):
                result = bestReptile['positions'][j] - etaPositions[i][j] * smallNumber - reducedPositions[i][j] * random.uniform(0,1)
                results.append(result)
            rets.append(results)
            results = []
        return rets

class ReptileSearchAlgorithm:
    def __init__(self, optimizerParameters, testFunctionParameters, testFunctionID):
        self.maxIter = optimizerParameters['maxIter']
        self.populationSize = optimizerParameters['populationSize']
        self.smallNumber = optimizerParameters['smallNumber']
        self.alpha = optimizerParameters['alpha']
        self.testFunctionParameters = testFunctionParameters
        self.testFunctionID = testFunctionID
    
    def evolutionarySense(self):
        return 2 * random.randint(-1,1) * (1 - (1/self.maxIter))
    
    def sumPositions(self, population):
        positions = []
        for reptile in population:
            positions.append(reptile['positions'])
        return np.sum(np.array(positions), axis=0)
    
    def percentageDifference(self, bestReptile, population):
        ret = []; positions = []
        for i in range(len(population)):
            for j in range(self.testFunctionParameters['dimension']):
                if self.sumPositions(population)[j] == 0:
                    averagePosition = population[i]['positions'][j] / self.smallNumber
                else:
                    averagePosition = population[i]['positions'][j] / self.sumPositions(population)[j]
                res = (population[i]['positions'][j] - averagePosition) / (bestReptile['positions'][j] * (self.testFunctionParameters['ranges'][1] - self.testFunctionParameters['ranges'][0]) + self.smallNumber)
                positions.append(self.alpha + res)
            ret.append(positions)
            positions = []
        return ret
            
    def eta(self, bestReptile, population):
        ret = []; eta = []
        differencePositions = self.percentageDifference(bestReptile, population)
        for i in range(self.populationSize):
            for j in range(self.testFunctionParameters['dimension']):
                eta.append(bestReptile['positions'][j] * differencePositions[i][j])
            ret.append(eta)
            eta = []
        return ret
    
    def reduce(self, bestReptile, population):
        ret = []; reduces = []
        for _ in range(self.populationSize):
            r2 = random.randint(0, self.populationSize-1)
            x_r2j = population[r2]
            for j in range(self.testFunctionParameters['dimension']):
                result = (bestReptile['positions'][j] - x_r2j['positions'][j]) / (bestReptile['positions'][j] + self.smallNumber)
                reduces.append(result)
            ret.append(reduces)
            reduces = []
        return ret
    
    def normalizedPositions(self, positions):
        for i in range(self.populationSize):
            for j in range(self.testFunctionParameters['dimension']):
                if positions[i][j] < self.testFunctionParameters['ranges'][0]:
                    positions[i][j] = self.testFunctionParameters['ranges'][0]
                if positions[i][j] > self.testFunctionParameters['ranges'][1]:
                    positions[i][j] = self.testFunctionParameters['ranges'][1]
        return positions
    
    def calcObjectiveFunction(self, positions):
        rets = []
        for i in range(self.populationSize):
            objectiveValue = MultimodalFunctionsFactory.initializingMultimodalFunctions(self.testFunctionID, positions[i])
            reptile = {
                'objectiveValue': objectiveValue,
                'positions': positions[i],
                'fitnessValue': MetaheuristicHelper(
                                    None,None,None,None,None
                                ).fitnessFunction(objectiveValue)
            }
            rets.append(reptile)
        return rets
    
    def runRSA(self, population):
        bestID = 0
        bestReptile = {
            'objectiveValue':None,
            'positions':None,
            'fitnessValue': 0
        }
        bestConvergences = []; objValues = []
        for iter in range(self.maxIter):

            # 1. get bestReptile
            population = sorted(population, key=lambda x: x['fitnessValue'], reverse=True)
            
            # 2. Update solutions
            etaPositions = self.eta(population[bestID], population)
            
            # 3. Update reduce functions
            reducedPositions = self.reduce(population[bestID], population)
            
            walking = WalkingMovementStrategy(
                self.alpha,
                self.maxIter)
            
            # 4. High walking
            if iter <= (self.maxIter/4): 
                positions = walking.highWalking(population[bestID], etaPositions, reducedPositions)
            
            # 5. Belly walking
            elif iter <= 2 * (self.maxIter/4) and iter > (self.maxIter / 4):
                positions = walking.bellyWalking(population[bestID], population)
            
            # 6. Hunting coordination
            elif iter <= 3 * (self.maxIter/4) and iter > 2 * (self.maxIter/4):
                positions = walking.huntingCoordination(population[bestID], self.percentageDifference(population[bestID], population))
            
            # 7. Hunting cooperation
            else:
                positions = walking.huntingCooperation(population[bestID], etaPositions, reducedPositions, self.smallNumber)
            
            population = self.calcObjectiveFunction(self.normalizedPositions(positions))
            population = sorted(population, key=lambda x: x['fitnessValue'], reverse=True)
            bestConvergences.append(bestReptile['fitnessValue'])
            if population[bestID]['fitnessValue'] > bestReptile['fitnessValue']:
                bestReptile = copy.deepcopy(population[bestID])
                
        return {
            'bestSolution':bestReptile, 
            'bestConvergence':bestConvergences
        }