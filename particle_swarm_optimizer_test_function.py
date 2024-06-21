from helper import MetaheuristicHelper as metaHelper
from testfunctions.multimodal import MultimodalFunctionsFactory
import random, sys, copy

class ParticleSwarmOptimizer:
    def __init__(self, optimizerParameters, testFunctionParameters, testFunctionID):
        self.maxIter = optimizerParameters['maxIter']
        self.optimizerParameters = optimizerParameters
        self.testFunctionParameters = testFunctionParameters
        self.testFunctionID = testFunctionID
    
    def fitnessFunction(self, objectiveValue):
        smallNumber = 0.0001
        return 1 / (objectiveValue + smallNumber)
    
    def createPositions(self):
        rets = []
        for _ in range(self.testFunctionParameters['dimension']):
            rets.append(random.uniform(self.testFunctionParameters['ranges'][0], self.testFunctionParameters['ranges'][1]))
        return rets
    
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
            objectiveValue = MultimodalFunctionsFactory.initializingMultimodalFunctions(self.testFunctionID, positions)
            particle = {
                'positions':positions,
                'velocities':self.createInitialVelocities(positions),
                'objectiveValue': objectiveValue, 
                'fitnessValue': metaHelper(
                                    None,None,None,None,None
                                ).fitnessFunction(objectiveValue)
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
        for i in range(self.testFunctionParameters['dimension']):
            self.testFunctionParameters['ranges'][1]
            position = positions[i] + velocities[i]
            if position < self.testFunctionParameters['ranges'][0]:
                position = self.testFunctionParameters['ranges'][0]
            if position > self.testFunctionParameters['ranges'][1]:
                position = self.testFunctionParameters['ranges'][1]
            positions[i] = position
        return positions
    
    def isUpdatePbest(self,pBest, particle):
        return particle['fitnessValue'] > pBest['fitnessValue']
    
    def runPSO(self, population, maxIter):
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
                objectiveValue = MultimodalFunctionsFactory.initializingMultimodalFunctions(self.testFunctionID, positions)
                particle = {
                    'objectiveValue': objectiveValue, 
                    'positions':positions,
                    'velocities':self.createInitialVelocities(positions),
                    'fitnessValue': metaHelper(None,None,None,None,None).fitnessFunction(objectiveValue)
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