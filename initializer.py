import random, sys

class Initializer:

  def __init__(self, designVariableRanges, dimension):
    self.designVariableRanges = designVariableRanges
    self.dimension = dimension

  def getPosition(self):

    positions = []

    for i in range(self.dimension):

      if self.dimension == len(self.designVariableRanges):
        randomValue = random.uniform(0, 1) * (self.designVariableRanges[i][1] - self.designVariableRanges[i][0]) + self.designVariableRanges[i][0]
        while(randomValue < self.designVariableRanges[i][0] or randomValue > self.designVariableRanges[i][1]):
          randomValue = random.uniform(0, 1) * (self.designVariableRanges[i][1] - self.designVariableRanges[i][0]) + self.designVariableRanges[i][0]
      else:
        randomValue = random.uniform(0, 1) * (self.designVariableRanges[0][1] - self.designVariableRanges[0][0]) + self.designVariableRanges[0][0]
        while(randomValue < self.designVariableRanges[0][0] or randomValue > self.designVariableRanges[0][1]):
          randomValue = random.uniform(0, 1) * (self.designVariableRanges[0][1] - self.designVariableRanges[0][0]) + self.designVariableRanges[0][0]

      positions.append(randomValue)

    return positions

  def createPopulation(self, popSize=30):

    population = []

    for _ in range(popSize):
      population.append(self.getPosition())


    return population