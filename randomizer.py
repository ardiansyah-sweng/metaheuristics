# sample 1d objective function
from numpy import arange
from numpy.random import seed
from numpy.random import rand
from matplotlib import pyplot
import matplotlib.pyplot as plt

# objective function
def objective(x):
	return x**2.0

# define range for input
r_min, r_max = -5.12, 5.12
# sample input range uniformly at 0.1 increments
inputs = arange(r_min, r_max, 0.1)
# summarize some of the input domain
#print(inputs[:100])
# compute targets
results = objective(inputs)
# summarize some of the results
#print(results[:100])
# simulate a sample made by an optimization algorithm
seed(1)
sample = r_min + rand(10) * (r_max - r_min)
# evaluate the sample
sample_eval = objective(sample)
# create a line plot of input vs result
pyplot.plot(inputs, results)
# define the known function optima
optima_x = 0.0
# evaluate the sample
sample_eval = objective(sample)
# plot the sample as black circles
pyplot.plot(sample, sample_eval, 'o', color='black')
print(sample)
print(sample_eval)
minSampleEval = min(sample_eval)
optima_y = objective(optima_x)
# draw the function optima as a red square
pyplot.plot([optima_x], [optima_y], 's', color='r')
# draw green dot for best solution
plt.annotate((round(sample[9],2), round(minSampleEval,2)), xy=(sample[9], minSampleEval), xytext=(1.1, 9), arrowprops=dict(facecolor='black', shrink=0.02),)
pyplot.plot(sample[9], minSampleEval, 'o', color='blue')
# show the plot
pyplot.show()

# create a mapping of some inputs to some results
# for i in range(5):
# 	print('f(%.3f) = %.3f' % (inputs[i], results[i]))