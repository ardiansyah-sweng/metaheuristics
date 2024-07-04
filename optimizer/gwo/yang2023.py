import random, copy, sys, math
import numpy as np
from ChaoticMaps import ChaoticMaps

class Yang2023:

  def __init__(self, params, objFunction, dimension, funcEval=0):
    self.params = params
    self.objFunction = objFunction
    self.dimension = dimension
    self.funcEval = funcEval

  def sortPopulation(self, population):

    #TODO <sort on the way, or at the end>
    for i in range(self.params['popSize']-1):
      for j in range(i+1, self.params['popSize']):
        
        objValue_i = self.objFunction.evaluate(population[i])
        objValue_j = self.objFunction.evaluate(population[j])
        self.funcEval += 2
        
        if  objValue_i > objValue_j:
          temp = population[i]
          population[i] = population[j]
          population[j] = temp
    
    return population

  def preyHunting(self, population, wolfType, C, A):

    for idx, wolf in enumerate(population):

      newVars = []

      for i in range(self.dimension):
        D = abs(C * wolfType[i] - wolf[i])
        newVar = wolfType[i] -  A * D

        #TODO <create particular class or helper>
        if newVar < self.params['designVariables'][i][0]:
          newVar = self.params['designVariables'][i][0]
        if newVar > self.params['designVariables'][i][1]:
          newVar = self.params['designVariables'][i][1]
        
        newVars.append(newVar)

        population[idx] = newVars
    
    return self.sortPopulation(population)

  def runGWO(self, population):

    currBestSolution = {
        'position': None,
        'fitnessValue': 1000
    }

    population = self.sortPopulation(population)

    a = 2.3
    R_k = 0.7

    for i in range(self.params['popSize']):
      randomVars = []

      R_k = (a * (R_k**2)) * math.sin(math.pi * R_k)

      for j in range(self.dimension):
        randomVar = R_k * (self.params['designVariables'][j][1] - self.params['designVariables'][j][0]) + self.params['designVariables'][j][0]

        while (randomVar < self.params['designVariables'][j][0] or randomVar > self.params['designVariables'][j][1]):
          randomVar = R_k * (self.params['designVariables'][j][1] - self.params['designVariables'][j][0]) + self.params['designVariables'][j][0]
        
        randomVars.append(randomVar)

      objValPop = self.objFunction.evaluate(population[i])
      objValChao = self.objFunction.evaluate(randomVars)
      self.funcEval += 2

      if objValPop > objValChao:
        population[i] = randomVars

    Mmin = 3
    MXupper = (Mmin + 1) * 10
    MXlower = Mmin

    if self.dimension <= (4 * self.params['popSize']):
      Mmax = round((self.dimension/self.params['popSize']) * (MXupper - MXlower) + MXlower)
    
    if self.dimension > (4 * self.params['popSize']):
      Mmax = Mmin

    leadersA = []; leadersC = []

    while self.funcEval < self.params['funcEvalLimit']:
      
      if self.funcEval < 3 / (4 * self.params['funcEvalLimit']):
        M = round(Mmax - self.funcEval * ((4 * (Mmax - Mmin)) / 3 * self.params['funcEvalLimit']))
      
      if self.funcEval >= 3 / (4 * self.params['funcEvalLimit']):
        M = Mmin
    
      print(M)
      sys.exit()

      coefficient = 2
      a = coefficient - (coefficient * self.funcEval) / self.params['funcEvalLimit']

      for _ in range(M):
        leadersA.append((coefficient * a) * random.uniform(0, 1) - a)
        leadersC.append(coefficient * random.uniform(0, 1))

      alphaA = (coefficient * a) * random.uniform(0, 1) - a
      betaA = (coefficient * a) * random.uniform(0, 1) - a
      deltaA = (coefficient * a) * random.uniform(0, 1) - a

      alphaC = coefficient * random.uniform(0, 1)
      betaC = coefficient * random.uniform(0, 1)
      deltaC = coefficient * random.uniform(0, 1)

      alphaIdx = 0; betaIdx = 1; deltaIdx = 2

      alphaWolf = population[alphaIdx]
      alphaPopulation = self.preyHunting(population, alphaWolf, alphaC, alphaA)

      betaWolf = population[betaIdx]
      betaPopulation = self.preyHunting(population, betaWolf, betaC, betaA)

      deltaWolf = population[deltaIdx]
      deltaPopulation = self.preyHunting(population, deltaWolf, deltaC, deltaA)

      for i in range(self.params['popSize']):
        positions = []
        for j in range(self.dimension):
          
          position = (alphaPopulation[i][j] + betaPopulation[i][j] + deltaPopulation[i][j]) / self.dimension

          if position < self.params['designVariables'][j][0]:
            position = self.params['designVariables'][j][0]
          if position > self.params['designVariables'][j][1]:
            position = self.params['designVariables'][j][1]

          positions.append(position)

        population[i] = positions
      
      alphaObjVal = self.objFunction.evaluate(alphaWolf)
      self.funcEval += 1
      print(self.funcEval)

      if alphaObjVal < currBestSolution['fitnessValue']:
        currBestSolution['position'] = copy.deepcopy(alphaWolf)
        currBestSolution['fitnessValue'] = copy.deepcopy(alphaObjVal)
      
      print(currBestSolution)
    