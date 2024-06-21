from use_case_points import UseCasePoint
from DatasetReader import readSilhavy71
from helper import MetaheuristicHelper
import random, sys, copy

class ParticleSwarmOptimizer:
    def __init__(self, optimizerParameters, objectiveFunctions, singleTupleDataset):
        self.designVariableRanges = objectiveFunctions['designVariableRanges']
        """
        output:\n
        {'lowerBound':5.00, 'upperBound':7.49},\n 
        {'lowerBound':7.50, 'upperBound':12.49}, \n
        {'lowerBound':12.50, 'upperBound':15.00}
        """
        self.singleTupleDataset = singleTupleDataset
        """
        output: [6.0, 10.0, 15.0, 9.0, 0.81, 0.84, 7970.0]
        """
        self.productivityFactor = objectiveFunctions['pf']
        self.maxIter = optimizerParameters['maxIter']
        self.optimizerParameters = optimizerParameters
        """contoh: \n
            'pso': {
                'inertiaMax': 0.9,
                'inertiaMin': 0.4,
                'c1':2,
                'c2':2
                },
        """
    
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
    
    def createInitialVelocities(self, positions):
        """_summary_

        Args:
            positions (_type_): _description_
        Output: [1.896437556109017, 5.787482119804733, 5.769010406574087]
        """
        velocities = []
        for positionValue in positions:
            velocities.append(positionValue * random.uniform(0,1))
        return velocities
        
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
                        'velocities':self.createInitialVelocities(positions),
                        'estimatedEffort':objectiveValues['estimatedEffort'], 
                        'absoluteError':objectiveValues['absoluteError'],
                        'fitnessValue':self.fitnessFunction(objectiveValues['absoluteErrorUUCW']),
                        'estimatedUUCW':objectiveValues['estimatedUUCW'],
                        'absoluteErrorUUCW':objectiveValues['absoluteErrorUUCW']
            }
            population.append(particle)
        return population
    
    def calcLDWInertia(self, iter):
        return self.optimizerParameters['inertiaMax'] - ((self.optimizerParameters['inertiaMax'] - self.optimizerParameters['inertiaMin'] * iter) / self.optimizerParameters['inertiaMax'])
    
    def updateVelocities(self, particle, pBests, gBest, inertia):
        """_summary_

        Args:
            particle (_type_): _description_
            pBests (_type_): _description_
            gBest (_type_): _description_
            inertia (_type_): _description_
        
        Output: [5.609236168739769, 2.9403990644182723, 2.1825909026972936]
        """
        r1 = random.uniform(0,1)
        r2 = random.uniform(0,1)
        velocities = []
        for i in range(len(particle['velocities'])):
          velocities.append(inertia * particle['velocities'][i] + 
                            self.optimizerParameters['c1'] * r1 * (pBests['positions'][i] - particle['positions'][i]) + self.optimizerParameters['c2'] * r2 * (gBest['positions'][i] - particle['positions'][i]))
        return velocities
    
    def getGbestParticle(self, population, colum): # TODO use another efficient sort algorithm
        """_summary_

        Args:
            population (_type_): _description_
            colum (_type_): _description_

        Returns:
            _type_: _description_ \n
            output: \n
            {'positions': [6.165049466235383, 12.089415448247788, 13.914179584235297], \n
            'velocities': [5.882072028661698, 0.20718262729802323, 6.788981964381633], \n
            'estimatedEffort': 5111.125949750855, \n
            'absoluteError': 2858.8740502491446, \n
            'fitnessValue': 0.0003497880450291427}
        """
        for i in range(len(population)):
            for j in range(i+1, len(population)):
                if population[i][colum['fitnessValue']] < population[j]['fitnessValue']:
                    temp = population[j]
                    population[j] = population[i]
                    population[i] = temp
        return population[colum['bestParticleIndex']]
    
    def updatingPositions(self, velocities, positions):
        """_summary_

        Args:
            velocities (_type_): _description_
            positions (_type_): _description_
        
        Output: [7.49, 12.188431323619776, 15.0]
        """
        for i in range(len(self.designVariableRanges)):
            self.designVariableRanges[i]['upperBound']
            position = positions[i] + velocities[i]
            if position < self.designVariableRanges[i]['lowerBound']:
                position = self.designVariableRanges[i]['lowerBound']
            if position > self.designVariableRanges[i]['upperBound']:
                position = self.designVariableRanges[i]['upperBound']
            positions[i] = position
        return positions
    
    def isUpdatePbest(self,pBest, particle):
        return particle['fitnessValue'] > pBest['fitnessValue']
    
    def runPSO(self, population, maxIter):
        column = {'fitnessValue':'fitnessValue', 'bestParticleIndex':0}
        bestID= 0 
        pBests = population
        gBest = sorted(population, key=lambda x: x['fitnessValue'], reverse=True)[bestID]
        tmpGbest = gBest
        bestConvergences = []
        # population update
        for iter in range(maxIter):
            inertia = self.calcLDWInertia(iter)
            for particleID in range(len(population)):
                velocities = self.updateVelocities(population[particleID], pBests[particleID], gBest, inertia)
                positions = self.updatingPositions(velocities, population[particleID]['positions'])
                objectiveValues = UseCasePoint.estimatingUCP(
                    self.singleTupleDataset,
                    self.productivityFactor,
                    positions
                )
                particle = {
                        'positions':positions,
                        'velocities':velocities,
                        'estimatedEffort':objectiveValues['estimatedEffort'], 
                        'absoluteError':objectiveValues['absoluteError'],
                        'fitnessValue':self.fitnessFunction(objectiveValues['absoluteError']),
                        'estimatedUUCW':objectiveValues['estimatedUUCW'],
                        'absoluteErrorUUCW':objectiveValues['absoluteErrorUUCW']
                }
                population[particleID] = particle
                if self.isUpdatePbest(pBests[particleID], particle):
                    pBests[particleID] = copy.deepcopy(particle)
            bestConvergences.append(gBest['fitnessValue'])
            gBest = sorted(pBests, key=lambda x: x['fitnessValue'], reverse=True)[bestID]
            if gBest['fitnessValue'] > tmpGbest['fitnessValue']:
                tmpGbest = copy.deepcopy(gBest)
        return {
            'bestSolution':gBest, 
            'bestConvergence':bestConvergences
        }         