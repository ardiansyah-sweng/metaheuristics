import numpy as np
from sklearn.model_selection import train_test_split, KFold, LeaveOneOut, LeavePGroupsOut, RepeatedKFold
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.utils import resample

class ModelEvaluator:

  def __init__(self, X, y, groups=None):
    self.X = X
    self.y = y
    self.groups = groups

  def trainTestSplit(self, classifier):

    X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=None)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    return mean_absolute_error(y_test, y_pred)

  def kFold(self, classifier, n_folds):

    kf = KFold(n_splits=n_folds, random_state=42, shuffle=True)
    fold_indices = kf.split(self.X, self.y)

    mae_scores = []

    for train_index, test_index in fold_indices:
        X_train, X_test = self.X.iloc[train_index], self.X.iloc[test_index]
        y_train, y_test = self.y.iloc[train_index], self.y.iloc[test_index]

        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        mae_scores.append(mean_absolute_error(y_test, y_pred))

    return np.mean(mae_scores)

  def loocv(self, classifier):

    loo = LeaveOneOut()
    mae_scores = []

    for train_index, test_index in loo.split(self.X):
      X_train, X_test = self.X.iloc[train_index], self.X.iloc[test_index]
      y_train, y_test = self.y.iloc[train_index], self.y.iloc[test_index]

      classifier.fit(X_train, y_train)
      y_pred = classifier.predict(X_test)
      mae_scores.append(mean_absolute_error(y_test, y_pred))

    return np.mean(mae_scores)

  def lgocv(self, classifier, p=2):

    if self.groups is None:
      raise ValueError("Groups must be provided for LGOCV")

    lpgo = LeavePGroupsOut(n_groups=p)
    mae_scores = []

    for train_index, test_index in lpgo.split(self.X, self.y, self.groups):
      X_train, X_test = self.X.iloc[train_index], self.X.iloc[test_index]
      y_train, y_test = self.y.iloc[train_index], self.y.iloc[test_index]

      if len(np.unique(y_train)) > 1:
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        mae_scores.append(mean_absolute_error(y_test, y_pred))

    if mae_scores:
      return np.mean(mae_scores)
    else:
      return None

  def repeatedKFold(self, classifier, n_splits=10, n_repeats=5):

    rkf = RepeatedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=42)
    mse_scores = []
    mae_scores = []

    for train_index, test_index in rkf.split(self.X, self.y):
      X_train, X_test = self.X.iloc[train_index], self.X.iloc[test_index]
      y_train, y_test = self.y.iloc[train_index], self.y.iloc[test_index]

      classifier.fit(X_train, y_train)
      y_pred = classifier.predict(X_test)

      mae_scores.append(mean_absolute_error(y_test, y_pred))

    return np.mean(mae_scores)

  def bootstrap(self, classifier, n_iterations=100):

    mae_scores = []

    for i in range(n_iterations):
      X_resampled, y_resampled = resample(self.X, self.y, random_state=i)
      out_of_sample_indices = np.setdiff1d(np.arange(len(self.X)), np.unique(X_resampled), assume_unique=True)
      X_out_of_sample, y_out_of_sample = self.X.iloc[out_of_sample_indices], self.y.iloc[out_of_sample_indices]

      classifier.fit(X_resampled, y_resampled)
      y_pred = classifier.predict(X_out_of_sample)
      mae_scores.append(mean_absolute_error(y_out_of_sample, y_pred))

    return np.mean(mae_scores)

  def optimism_bootstrap(self, classifier, n_iterations=100):

    mae_scores_in = []
    mae_scores_out = []

    for i in range(n_iterations):
      X_resampled, y_resampled = resample(self.X, self.y, random_state=i)
      out_of_sample_indices = np.setdiff1d(np.arange(len(self.X)), np.unique(X_resampled), assume_unique=True)
      X_out_of_sample, y_out_of_sample = self.X.iloc[out_of_sample_indices], self.y.iloc[out_of_sample_indices]

      classifier.fit(X_resampled, y_resampled)

      # In-sample accuracy
      y_pred_in = classifier.predict(X_resampled)
      accuracy_in = mean_absolute_error(y_resampled, y_pred_in)
      mae_scores_in.append(accuracy_in)

      # Out-of-sample accuracy
      y_pred_out = classifier.predict(X_out_of_sample)
      accuracy_out = mean_absolute_error(y_out_of_sample, y_pred_out)
      mae_scores_out.append(accuracy_out)

    mean_accuracy_in = np.mean(mae_scores_in)
    mean_accuracy_out = np.mean(mae_scores_out)
    optimism = mean_accuracy_in - mean_accuracy_out

    return mean_accuracy_out, optimism

  def boot362(self, classifier, n_iterations=100):

    mae_scores = []

    for i in range(n_iterations):
      X_resampled, y_resampled = resample(self.X, self.y, random_state=i)
      kf = KFold(n_splits=3, shuffle=True, random_state=42)
      fold_accuracies = []

      for train_index, test_index in kf.split(X_resampled):
        X_train, X_test = X_resampled.iloc[train_index], X_resampled.iloc[test_index]
        y_train, y_test = y_resampled.iloc[train_index], y_resampled.iloc[test_index]

        if len(np.unique(y_train)) > 1 and len(np.unique(y_test)) > 1:
          classifier.fit(X_train, y_train)
          y_pred = classifier.predict(X_test)
          accuracy = mean_absolute_error(y_test, y_pred)
          fold_accuracies.append(accuracy)
        else:
          continue

      if fold_accuracies:
        mean_fold_accuracy = np.mean(fold_accuracies)
        mae_scores.append(mean_fold_accuracy)

    return np.mean(mae_scores)

  def adaptiveBootstrap(self, classifier, n_iterations=100):

    mae_scores = []

    for i in range(n_iterations):
      X_resampled, y_resampled = self.adaptive_resample()
      classifier.fit(X_resampled, y_resampled)
      y_pred = classifier.predict(self.X)
      accuracy = mean_absolute_error(self.y, y_pred)
      mae_scores.append(accuracy)

    return np.mean(mae_scores)

  def adaptive_resample(self):
    n_samples = len(self.X)
    resample_indices = np.random.choice(n_samples, size=n_samples, replace=True)
    X_resampled = self.X.iloc[resample_indices]
    y_resampled = self.y.iloc[resample_indices]

    return X_resampled, y_resampled