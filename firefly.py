import random
from use_case_points import UseCasePoint
import sys, copy, math
from helper import MetaheuristicHelper

class FireflyOptimizer:
    def __init__(self, optimizerParameters, objectiveFunctions, singleTupleDataset):
        self.designVariableRanges = objectiveFunctions['designVariableRanges']
        self.singleTupleDataset = singleTupleDataset
        self.productivityFactor = objectiveFunctions['pf']
        self.maxIter = optimizerParameters['maxIter']
        self.populationSize = optimizerParameters['populationSize']
        self.FFParameters = optimizerParameters
        
    def createNewFF(self, positions):
        objectiveValue = UseCasePoint.estimatingUCP(
                self.singleTupleDataset,
                self.productivityFactor,
                positions
        )
        return {
            'positions': positions,
            'estimatedEffort': objectiveValue['estimatedEffort'],
            'absoluteError': objectiveValue['absoluteError'],
            'fitnessValue': MetaheuristicHelper(
                self.designVariableRanges,
                self.singleTupleDataset,
                self.productivityFactor,
                self.maxIter
            ).fitnessFunction(objectiveValue['absoluteError'])
    }
        
    def moveDimFFtoBrightFF(self, brightFF, dimFF):
        for i in range(len(self.designVariableRanges)):
            distance = math.sqrt((brightFF['positions'][i] - dimFF['positions'][i])**2)
            
            attractiveness = self.FFParameters['beta'] * math.exp(-self.FFParameters['gamma'] * (distance**2))
            
            randomEpsilon = random.randint(int(self.FFParameters['minEpsilon'] * 100), int(self.FFParameters['maxEpsilon'] * 100)) / 100
            
            dimFF['positions'][i] = dimFF['positions'][i] + attractiveness * (brightFF['positions'][i] - dimFF['positions'][i]) + self.FFParameters['alpha'] * randomEpsilon
            
            if dimFF['positions'][i] < self.designVariableRanges[i]['lowerBound']:
                dimFF['positions'][i] = self.designVariableRanges[i]['lowerBound']
            if dimFF['positions'][i] > self.designVariableRanges[i]['upperBound']:
                dimFF['positions'][i] = self.designVariableRanges[i]['upperBound']
                
        return self.createNewFF(dimFF['positions'])

    def runFirefly(self, population):
        bestFF = {
            'positions':None,
            'estimatedEffort':None,
            'absoluteError': None,
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