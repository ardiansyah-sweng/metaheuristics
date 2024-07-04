import math, random, sys, copy

class PSO:
    
    def __init__(self, params, objFunction):
        self.params = params
        self.objFunction = objFunction

    def createInitialVelocities(self):

        velocities = []

        for i in range(self.params['popSize']):
            
            velocity = []

            for j in range(len(self.params['designVariables'])):
                velocity.append(random.uniform(self.params['designVariables'][j][0], self.params['designVariables'][j][1]) * random.uniform(0,1))
            
            velocities.append(velocity)
        
        return velocities

    def calcLDWInertia(self, iter):
        inertiaMax = 0.9
        inertiaMin = 0.2
        return inertiaMax - ((inertiaMax - inertiaMin * iter) / inertiaMax)

    def updateVelocity(self, velocity, particle, pBest, gBest, inertia):

        r1 = random.uniform(0,1)
        r2 = random.uniform(0,1)

        velocities = []
        c1 = c2 = 2
        for i in range(len(self.params['designVariables'])):
          velocities.append(inertia * velocity[i] + 
                            c1 * r1 * (pBest[i] - particle[i]) + c2 * r2 * (gBest[i] - particle[i]))
        return velocities

    def updatingPositions(self, velocity, positions):

        for i in range(len(velocity)):

            position = positions[i] + velocity[i]

            if position < self.params['designVariables'][i][0]:
                position = self.params['designVariables'][i][0]
            if position > self.params['designVariables'][i][1]:
                position = self.params['designVariables'][i][1]
            
            positions[i] = position

        return positions

    def getBestSolution(self, population):

        objValues = []

        for i in range(self.params['popSize']):
            objValue = self.objFunction.evaluate(population[i])
            objValues.append(objValue)

        bestObjValue = min(objValues)
        bestObjValueIdx = objValues.index(bestObjValue)

        return population[bestObjValueIdx]

    def isUpdatePbest(self, pBest, particle):

        pBestValue = self.objFunction.evaluate(pBest)
        particleValue = self.objFunction.evaluate(particle)

        return particleValue > pBestValue

    def runPSO(self, population):

        currBestSolution = {
            'position': None,
            'fitnessValue': 1000
        }

        pBests = population
        gBest = self.getBestSolution(population)
        velocities = self.createInitialVelocities()

        for iter in range(self.params['maxIter']):
            inertia = self.calcLDWInertia(iter)
            for i in range(self.params['popSize']):
                velocity = self.updateVelocity(velocities[i], population[i], pBests[i], gBest, inertia)
                velocities[i] = copy.deepcopy(velocity)
                positions = self.updatingPositions(velocity, population[i])

                population[i] = copy.deepcopy(positions)

                if self.isUpdatePbest(pBests[i], population[i]):
                    pBests[i] = copy.deepcopy(population[i])
                
            gBest = self.getBestSolution(pBests)

            gBestVal = self.objFunction.evaluate(gBest)
            
            if gBestVal < currBestSolution['fitnessValue']:
                currBestSolution['position'] = copy.deepcopy(gBest)
                currBestSolution['fitnessValue'] = copy.deepcopy(gBestVal)

            print(currBestSolution )

        sys.exit()

