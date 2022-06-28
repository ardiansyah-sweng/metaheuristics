import numpy as np
from numpy.random import seed
from numpy.random import rand
from matplotlib import pyplot
import matplotlib.pyplot as plt
from numpy import arange
from numpy import sin
from matplotlib.animation import FuncAnimation
import sys

# Objective function
def f(x):
    #return x**2.0
    return sin(x) + sin((10.0 / 3.0) * x)
    
# Define input range
# xMin, xMax = -5.12, 5.12
xMin, xMax = -2.7, 7.5

# Parameter PSO
c1 = c2 = 2
w = 0.8
maxIter = 50
best = []
pos = []
fitness = []

# create initial particles
# seed(6)
numOfParticle = 30
xInitial = xMin + rand(numOfParticle) * (xMax - xMin)
initialFitness = f(xInitial)
# sample input range uniformly at 0.1 increments
inputs = arange(xMin, xMax, 0.1)

# compute targets
results = f(inputs)

def checkPbestFitness(pbestFitness, xFitness):
    ret = []
    for x in range(len(pbestFitness)):
        if (pbestFitness[x] < xFitness[x]):
            ret.append(pbestFitness[x])
        else:
            ret.append(xFitness[x])
    return ret

def checkPbestX(pbestFitness, pbestX, xFitness, X):
    ret = []
    for i in range(len(pbestFitness)):
        if ([pbestFitness[i]] == xFitness[i]):
           ret.append(X[i])
        else:
            ret.append(pbestX[i])
    return ret

def updateVelocity(V, pbestX, X, gbest,):
    return w * V + c1 * r1 * (pbestX - X) + c2 * r2 * (gbest - X)

def checkLimit(X):
    ret = []
    for x in X:
        if(x < xMin):
            ret.append(xMin)
        if(x > xMax):
            ret.append(xMax)
        if(x > xMin and x < xMax):
            ret.append(x)
    return ret

for i in range(maxIter+1):
    r1, r2 = np.random.rand(2)
    if (i==0):
        pbestX = xInitial
        pbestFitness = np.array([f(pbestX), pbestX])
        gbest = np.where(pbestFitness[0] == min(pbestFitness[0]))
        V = np.random.random(numOfParticle)
        particles = np.array([xInitial, V, pbestX, pbestX[gbest[0][0]], pbestFitness[0]])
    if (i > 0):
        V = updateVelocity(particles[1], particles[2], particles[0], particles[3])
        X = particles[0] + V
        X = np.asarray(checkLimit(X))
        # sys.exit()
        xFitness = f(X)
        pbestFitness = checkPbestFitness(xFitness, particles[4])
        pbestX = checkPbestX(pbestFitness, particles[2], xFitness, X)
        gbest = np.where(pbestFitness == min(pbestFitness))
        particles = np.array([X, V, pbestX, pbestX[gbest[0][0]], xFitness, min(pbestFitness)])
        best.append(particles[5])
        pos.append(particles[3])

gBest = np.where(best == min(best))
print("Best", min(best))
print("x = ", pos[gBest[0][0]])

## Plot
optimaX = 5.145735
optimaY = f(optimaX)

plt.figure()
plt.subplot(211)
pyplot.plot(inputs, results)
pyplot.plot(xInitial, initialFitness, 'o', color = 'black')
pyplot.plot([optimaX], [optimaY], 's', color='r')
plt.xlabel("Position (x)")
plt.ylabel("f(x) = sin(x) + sin((10.0 / 3.0) * x)")

plt.subplot(212)
pyplot.plot(inputs, results)
pyplot.plot(pos, best, 'o', color = 'black')
pyplot.plot([optimaX], [optimaY], 's', color='r')
pyplot.plot(pos[gBest[0][0]], min(best), 'o', color='blue')
plt.xlabel("Position (x)")
plt.ylabel("f(x) = sin(x) + sin((10.0 / 3.0) * x)")
plt.text(4, 1, (round(pos[gBest[0][0]],5), round(min(best),9)) )

pyplot.show()