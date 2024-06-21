from use_case_points import UseCasePoint
from testfunctions.multimodal import MultimodalFunctionsFactory
import random, sys

class MetaheuristicHelper:
    def __init__(self, designVariableRanges, singleTupleDataset, productivityFactor, maxIter, numOfDimension):
        self.designVariableRanges = designVariableRanges
        self.singleTupleDataset = singleTupleDataset
        self.productivityFactor = productivityFactor
        self.maxIter = maxIter
        self.numOfDimension = numOfDimension
        
    def fitnessFunction(self, objectiveValue):
        smallNumber = 0.0001
        return 1 / (objectiveValue + smallNumber)
    
    def createPositions(self):
        """_summary_

        Returns:
            _type_: _description_
            output: [6.34, 8.99, 14.65]
        """
        positions = []
        for designVariableRange in self.designVariableRanges:
            positions.append(random.uniform(designVariableRange['lowerBound'], designVariableRange['upperBound']))
        return positions
    
    def createTestFunctionPositions(self):
        positions = []
        for _ in range(self.numOfDimension):
            positions.append(random.uniform(self.designVariableRanges[0], self.designVariableRanges[1]))
        return positions
    
    def generateTestFunctionInitialPopulation(self, populationSize, testFunctionID):
        population = []
        for _ in range(populationSize):
            variableValues = self.createTestFunctionPositions()
            objectiveValue = MultimodalFunctionsFactory.initializingMultimodalFunctions(testFunctionID, variableValues)
            population.append({
                'fitnessValue': self.fitnessFunction(objectiveValue),
                'objectiveValue':objectiveValue, 
                'positions':variableValues
            })
        return population
    
    def generateInitialPopulation(self, populationSize):
        """_summary_

        Returns:
            _type_: _description_ \n
            output: \n
            [
                {'positions': [5.555677670971859, 12.340278296728709, 12.990146799843153], \n
                'velocities': [3.0781011735895984, 9.731113776413016, 7.374408175420374],\n
                'estimatedEffort': 4906.895805882337, \n
                'absoluteError': 3063.1041941176627, \n
                'fitnessValue': 0.00032646619376309983}, \n
                ... \n
                }
            ]
        """
        population = []
        for _ in range(populationSize):
            positions = self.createPositions()
            objectiveValues = UseCasePoint.estimatingUCP(
                self.singleTupleDataset,
                self.productivityFactor,
                positions
            )
            particle = {'positions':positions,
                        'estimatedEffort':objectiveValues['estimatedEffort'], 
                        'absoluteError':objectiveValues['absoluteError'],
                        'fitnessValue':self.fitnessFunction(objectiveValues['absoluteError']),
                        'estimatedUUCW':objectiveValues['estimatedUUCW'],
                        'absoluteErrorUUCW':objectiveValues['absoluteErrorUUCW']
            }
            population.append(particle)
        return population

    def generateSeedsPopulation(self, dataSeeds):
        """_summary_

        Returns:
            _type_: _description_ \n
            output: \n
            [
                {'positions': [5.555677670971859, 12.340278296728709, 12.990146799843153], \n
                'velocities': [3.0781011735895984, 9.731113776413016, 7.374408175420374],\n
                'estimatedEffort': 4906.895805882337, \n
                'absoluteError': 3063.1041941176627, \n
                'fitnessValue': 0.00032646619376309983}, \n
                ... \n
                }
            ]
        """
        seedsPopulation = []; rets = []
        for i in range(len(dataSeeds)):
            population = []
            for j in range(len(dataSeeds[i])):
                objectiveValues = UseCasePoint.estimatingUCP(
                    self.singleTupleDataset,
                    self.productivityFactor,
                    dataSeeds[i][j]
                )
                particle = {'positions':dataSeeds[i][j],
                            'estimatedEffort':objectiveValues['estimatedEffort'], 
                            'absoluteError':objectiveValues['absoluteError'],
                            'fitnessValue':self.fitnessFunction(objectiveValues['absoluteError']),
                            'estimatedUUCW':objectiveValues['estimatedUUCW'],
                            'absoluteErrorUUCW':objectiveValues['absoluteErrorUUCW']
                }
                population.append(particle)
            seedsPopulation.append(population)
            population = []
            
        return seedsPopulation