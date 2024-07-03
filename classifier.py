from model_evaluator import ModelEvaluator
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split, LeaveOneOut
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, make_scorer
import numpy as np
from scipy.stats import uniform, randint


class Classifier():
  def __init__(self):
    pass

  def evaluate(self, X):
    raise NotImplementedError("Subclass must implement abstract method.")

class SVRegression(Classifier):

  def __init__(self, X, y, groups, dimension):
    self.X = X
    self.y = y
    self.groups = groups
    self.dimension = dimension

  def evaluate(self, penaltyGamma):

    evaluator = ModelEvaluator(self.X, self.y, self.groups)

    accuracy = evaluator.loocv(SVR(C=penaltyGamma[0], kernel='rbf', gamma=penaltyGamma[1]))

    # accuracy = evaluator.trainTestSplit(SVR(C=penaltyGamma[0], kernel='rbf', gamma=penaltyGamma[1]))
    #accuracy = evaluator.kFold(SVR(C=penaltyGamma[0], kernel='linear', gamma=penaltyGamma[1]), n_folds=5)

    return accuracy

class GridSVRShukla2023(Classifier):

  def __init__(self, X, y):
    self.X = X
    self.y = y  

  def evaluate(self):
    
    param_grid = {
      'kernel': ['rbf'],
      'C': [200],
      'gamma': [0.01],
      'epsilon': [0.0001]
    }

    svr = SVR()
    loo = LeaveOneOut()

    scorers = {
      'neg_mean_squared_error': 'neg_mean_squared_error',
      'mean_absolute_error': make_scorer(mean_absolute_error, greater_is_better=False)
    }

    grid_search = GridSearchCV(estimator=svr, param_grid=param_grid, cv=loo, scoring=scorers, refit='neg_mean_squared_error')
    grid_search.fit(self.X, self.y)

    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(self.X)

    mae = mean_absolute_error(self.y, y_pred)
    mse = mean_squared_error(self.y, y_pred)
    print(mae, mse)

class RandomSVRShukla2023(Classifier):

  def __init__(self, X, y):
    self.X = X
    self.y = y  

  def evaluate(self):
    
    param_distributions = {
      'kernel': ['rbf'],
      'C': [200],
      'gamma': [0.01],
      'epsilon': [0.0001]
    }

    svr = SVR()
    loo = LeaveOneOut()

    scorers = {
      'neg_mean_squared_error': 'neg_mean_squared_error',
      'mean_absolute_error': make_scorer(mean_absolute_error, greater_is_better=False)
    }

    random_search = RandomizedSearchCV(estimator=svr, param_distributions=param_distributions, n_iter=100, cv=loo, scoring=scorers, refit='neg_mean_squared_error')
    random_search.fit(self.X, self.y)

    best_model = random_search.best_estimator_
    y_pred = best_model.predict(self.X)

    mae = mean_absolute_error(self.y, y_pred)
    mse = mean_squared_error(self.y, y_pred)
    
    return [mae, mse]

class GridSVRegression(Classifier):
  
  def __init__(self, X, y):
    self.X = X
    self.y = y

  def evaluate(self):

    scaler = StandardScaler()

    svr = SVR()

    pipeline = Pipeline([
      ('scaler', scaler),
      ('svr', svr)
    ])
    
    n_features = self.X.shape[1]

    gamma_auto = 1 / n_features

    param_grid = {
      'svr__kernel': ['rbf'],
      'svr__C': [200],
      'svr__gamma': [0.01],
      'svr__epsilon': [0.0001]
      # 'svr__degree': [2, 3, 4],
      # 'svr__coef0': [0.0, 0.5, 1.0]
    }

    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='neg_mean_absolute_error')

    grid_search.fit(self.X, self.y)
    #print("Best parameters found: ", grid_search.best_params_)
    # print("Best cross-validation score: ", grid_search.best_score_)  
    
    X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=None)
    y_pred = grid_search.best_estimator_.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print("Mean Absolute Error on testing data: ", mae)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error on testing data: ", mse)

    print(y_test)
    print(y_pred)
    
    # Cetak nilai aktual dan prediksi
    print("\nAktual\t\tPrediksi")
    print("=====================")
    # for i in range(len(y_test)):
    #   print(f"{y_test[i]:.2f}\t\t{y_pred[i]:.2f}")

class RandomSVRegression(Classifier):
  
  def __init__(self, X, y):
    self.X = X
    self.y = y

  def evaluate(self):

    scaler = StandardScaler()

    svr = SVR()

    pipeline = Pipeline([
      ('scaler', scaler),
      ('svr', svr)
    ])
    
    n_features = self.X.shape[1]

    gamma_auto = 1 / n_features

    print("Nilai gamma ketika diatur ke 'auto':", gamma_auto)

    param_dist = {
      'svr__kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
      'svr__C': [200],
      'svr__gamma': [0.01],
      'svr__degree': [2, 3, 4],
      'svr__coef0': [0.0, 0.5, 1.0]
    }

    random_search = RandomizedSearchCV(pipeline, param_dist, n_iter=100, cv=5, scoring='neg_mean_absolute_error', random_state=42)

    random_search.fit(self.X, self.y)
    print("Best parameters found: ", random_search.best_params_)
    print("Best cross-validation score: ", random_search.best_score_)    
    
    X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
    y_pred = random_search.best_estimator_.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print("Mean Absolute Error on testing data: ", mae)

    print(y_test)
    print(y_pred)
    
    # Cetak nilai aktual dan prediksi
    print("\nAktual\t\tPrediksi")
    print("=====================")
    # for i in range(len(y_test)):
    #   print(f"{y_test[i]:.2f}\t\t{y_pred[i]:.2f}")


