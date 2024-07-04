import math, copy, random, sys

class Firefly:

  def __init__(self, params, objFunction):
    self.params = params
    self.objFunction = objFunction

  def moveDimFFtoBrightFF(self, brightFF, dimFF):
    alpha = 0.
    beta = 1
    betaMin = 0.5
    gamma = 1
    minEpsilon = -5
    maxEpsilon = 5

    for i in range(len(brightFF)):
      distance = math.sqrt((brightFF[i] - dimFF[i])**2)
      attractiveness = beta * math.exp(-gamma * (distance**2))
      randomEpsilon = random.randint(int(minEpsilon * 100), int(maxEpsilon * 100)) / 100
      dimFF[i] = dimFF[i] + attractiveness * (brightFF[i] - dimFF[i]) + alpha * randomEpsilon

      if dimFF[i] < self.params['designVariables'][i][0]:
        dimFF[i] = self.params['designVariables'][i][0]
      if dimFF[i] > self.params['designVariables'][i][1]:
        dimFF[i] = self.params['designVariables'][i][1]

    return dimFF

  #TODO <create particular class to be accessed by all optimizer. Write once access anywhere>
  def getBestSolution(self, population):

    objValues = []

    for i in range(self.params['popSize']):
      objValue = self.objFunction.evaluate(population[i])
      objValues.append(objValue)

    bestObjValue = min(objValues)
    bestObjValueIdx = objValues.index(bestObjValue)

    return population[bestObjValueIdx]

  def runFirefly(self, population):

    currBestSolution = {
        'position': None,
        'fitnessValue': 1000
    }

    for _ in range(self.params['maxIter']):
      for j in range(self.params['popSize']):
        for k in range(self.params['popSize']):
          if self.objFunction.evaluate(population[k]) > self.objFunction.evaluate(population[j]):
            population[j] = self.moveDimFFtoBrightFF(population[k], population[j])

      bestSolution = self.getBestSolution(population)
      bestFitnessValue = self.objFunction.evaluate(bestSolution)

      if bestFitnessValue < currBestSolution['fitnessValue']:
        currBestSolution['position'] = bestSolution
        currBestSolution['fitnessValue'] = bestFitnessValue
      
      print(currBestSolution)
    sys.exit()