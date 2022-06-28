# unimodal test function
from numpy import arange
from numpy import meshgrid
import numpy as np
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import math
import sys

# objective function
def objective(x, y):
    #Sphere
	#return x**2.0 + y**2.0
 
	#Schwefel 2.22
	#return (abs(x) + np.dot(x,y)) + (abs(x) + np.dot(x,y))

	#Schwefel 1.20
	#return (x**2 + (x + x)**2) + (y**2 + (y + y)**2)
	
	#Schwefel 2.21
	print(y)
	sys.exit()
	#Rosenbrock
	# return 100 * (y - x**2)**2 + (x - 1)**2
 
	#Step
	# return ((x + 0.5)**2) + ((x + 0.5)**2)
 
	#Quartic Noise
	# return (x**4 + np.random.rand(1)) + (2*(y**4) + np.random.rand(1))
 
	#Schwefel 2.26

	#Rastrigin
	

# define range for input
r_min, r_max = -10, 10
# sample input range uniformly at 0.1 increments
xaxis = arange(r_min, r_max, 0.1)
yaxis = arange(r_min, r_max, 0.1)
# create a mesh from the axis
x, y = meshgrid(xaxis, yaxis)
# compute targets
results = objective(x, y)
# create a surface plot with the jet color scheme
figure = pyplot.figure()
axis = figure.gca(projection='3d')
axis.plot_surface(x, y, results, cmap='jet')
# show the plot
pyplot.show()