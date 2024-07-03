from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.utils import shuffle
import pandas as pd
from initializer import Initializer
from classifier import SVRegression, GridSVRegression, RandomSVRegression, GridSVRShukla2023, RandomSVRShukla2023
from ff import Firefly
from pso_hpo import PSO

path = "UCP.xlsx"
df = pd.read_excel(path)

X = df.drop(columns=['Project_No', 'UUCP', 'UCP'])
y = df['UCP']
groups = df['UCP']

designVariables = [
    [0.01, 200],
    [0.01, 50]
]

dimension = 2

params = {
    'popSize': 10,
    'maxIter': 15,
    'designVariables': [
        [0.01, 200],
        [0.01, 50]
    ]
}

initialPopGenerator = Initializer(designVariables, dimension)
population = initialPopGenerator.createPopulation(params['popSize'])

#objFunction = Schwefel()

#objFunction = GridSVRegression(X, y).evaluate()
#objFunction = RandomSVRegression(X, y).evaluate()
#objFunction = GridSVRShukla2023(X, y).evaluate()
objFunction = RandomSVRShukla2023(X, y).evaluate()
print(objFunction)

objFunction = SVRegression(X, y, groups, dimension)
# ff = Firefly(params, objFunction)
# ff.runFirefly(population)

pso = PSO(params, objFunction)
pso.runPSO(population)

#models = [
    # KNeighborsRegressor(n_neighbors=3, leaf_size=20),
    # SVR(C=0.2, kernel='rbf', gamma=10),
    #DecisionTreeRegressor(random_state=42)
    #MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42)
    #RandomForestRegressor(n_estimators=100, random_state=42)
    #GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
#]

# accuracies = []
# for i in range(len(models)):
#     accuracies.append(evaluator.trainTestSplit(models[i]))
#     accuracies.append(evaluator.kFold(models[i], n_folds=5))
#     accuracies.append(evaluator.loocv(models[i]))
#     accuracies.append(evaluator.lgocv(models[i], p=2))
#     accuracies.append(evaluator.repeatedKFold(models[i], n_splits=10, n_repeats=5))
#     accuracies.append(evaluator.bootstrap(models[i], n_iterations=100))
#     accuracies.append(evaluator.optimism_bootstrap(models[i], n_iterations=100))
#     accuracies.append(evaluator.boot362(models[i], n_iterations=100))
#     accuracies.append(evaluator.adaptiveBootstrap(models[i], n_iterations=100))
# print(accuracies)