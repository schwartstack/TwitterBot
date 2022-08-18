import sklearn.metrics

from BandNameBot import BandNameBot
from BoardgameBot import BoardgameBot
from TwitterBot import TwitterBot
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import tweepy
    import schedule
    import time
    from datetime import date, datetime
    import pandas as pd
    import numpy as np
    import requests
    from bs4 import BeautifulSoup
    import random
    import sys
    import re
    import readline
    import os
    import traceback
#
# iris = pd.read_csv("~/Documents/Python Programming/iris.csv").drop('Unnamed: 0', axis=1)
# X = iris.iloc[0:149, 0:3]
# y = iris.iloc[0:149, 4]

#
# def predict_classification(X, y, model, nfolds=3):
#     X = pd.get_dummies(X)
#     pred = np.repeat(None, len(y))
#     split = np.random.choice(np.arange(nfolds), len(y), replace=True)
#     for fold in np.arange(nfolds):
#         model.fit(X[split != fold], y[split != fold])
#         pred[split == fold] = model.predict(X[split == fold])
#     return pred
#
# data = pd.read_csv("~/Desktop/data1.csv")
# # data = pd.read_csv("~/Desktop/data2.csv")
#
# X = data.drop("y", axis=1)
# y = data.y
# #
# # from sklearn.ensemble import RandomForestClassifier
# # from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# #
# # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=24)
# classifier = LogisticRegression()
# pred = predict_classification(X, y, classifier, 3)
# print(np.mean(pred == y))
#
# # classifier.fit(X_train, y_train)
# #
# # # Here X_test, y_test are the test data points
# # predictions = classifier.predict(X_test)
# # print(predictions)
# # # print(predictions)
# # # print(y_test)
# #
# # def report(f, pred, y):
# #     print(f.__name__ + " = " + str(f(pred, y)))
# #
# # #
# # #
# # #
# # # Accuracy
# # from sklearn.metrics import accuracy_score
# # report(accuracy_score, predictions, y_test)
# # #
# # # BalancedAccuracy
# # from sklearn.metrics import balanced_accuracy_score
# # report(balanced_accuracy_score, predictions, y_test)
# # #
# # # Recall
# # from sklearn.metrics import recall_score
# # # # ‘micro’, ‘macro’, ‘samples’, ‘weighted’
# # # print(recall_score(y_true=y_test, y_pred=predictions, average='micro')) #same as accuracy
# # # print(recall_score(y_true=y_test, y_pred=predictions, average='macro'))
# # # # print(recall_score(y_true=y_test, y_pred=predictions, average='samples'))
# # # print(recall_score(y_true=y_test, y_pred=predictions, average='weighted')) #same as accuracy
# # # #
# # from sklearn.metrics import precision_score
# # # print(precision_score(y_true=y_test, y_pred=predictions, average='micro')) #same as accuracy
# # # print(precision_score(y_true=y_test, y_pred=predictions, average='macro')) #same as balanced accuracy
# # # # print(recall_score(y_true=y_test, y_pred=predictions, average='samples'))
# # # print(precision_score(y_true=y_test, y_pred=predictions, average='weighted'))
# # from sklearn.metrics import f1_score
# # def precision(pred, y):
# #     return precision_score(y_true=y, y_pred=pred, average='weighted')
# # def recall(pred, y):
# #     return recall_score(y_true=y, y_pred=pred, average='macro')
# #
# # report(precision, predictions, y_test)
# # report(recall, predictions, y_test)
# #
# # print(f1_score(y_true=y_test, y_pred=predictions, average='micro')) #same as accuracy
# # print(f1_score(y_true=y_test, y_pred=predictions, average='macro'))
# # print(f1_score(y_true=y_test, y_pred=predictions, average='weighted')) #close to precision
# #
# # from sklearn.metrics import cohen_kappa_score
# # print(cohen_kappa_score(y_test, predictions))
# # print(cohen_kappa_score(y_test, predictions))
# # print(cohen_kappa_score(y_test, predictions))
#
#
# # print(recall_score(predictions, y_test, pos_label='virginica'))
# # print(recall_score(predictions, y_test, pos_label='versicolor'))
# # from sklearn.metrics import classification_report
# # print(classification_report(y_test, predictions))
#
# # # Sensitivity
#
# #
# #
# # # Specificity
# # # Precision
# # # F1Score
# # # Kappa
# #
# #
# #
# # print(np.mean(predictions == y_test))
#

bot = BandNameBot()
bot.tweet()