import copy
from xgboost import XGBClassifier, XGBRegressor
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM

def cmre(treatment, outcome, covariates, normal_dataset, strategic_dataset):

    # Variables used by main model to predict anchor
    v = copy.deepcopy(covariates)
    v.append(treatment)
    
    train_strategic_df, test_strategic_df = train_test_split(strategic_dataset, test_size=0.2, random_state=42)

    # Split the strategic dataset
    strategic_df_1 = test_strategic_df[test_strategic_df[treatment] == 1]
    strategic_df_0 = test_strategic_df[test_strategic_df[treatment] == 0]

    # Train the models using the train split
    normal_model = XGBRegressor().fit(normal_dataset[v], normal_dataset[outcome])
    strategic_model = XGBRegressor().fit(train_strategic_df[v], train_strategic_df[outcome])

    # Estimate the CATEs
    normal_ce_1 = normal_model.predict(strategic_df_1[covariates].assign(**{treatment: 1})[v]) \
                - normal_model.predict(strategic_df_1[covariates].assign(**{treatment: 0})[v])
    normal_ce_0 = normal_model.predict(strategic_df_0[covariates].assign(**{treatment: 1})[v]) \
                - normal_model.predict(strategic_df_0[covariates].assign(**{treatment: 0})[v])
    strategic_ce_1 = strategic_model.predict(strategic_df_1[covariates].assign(**{treatment: 1})[v]) \
                - strategic_model.predict(strategic_df_1[covariates].assign(**{treatment: 0})[v])    
    
    # Estimate the misreporting rate
    mr = (np.mean(normal_ce_1) - np.mean(strategic_ce_1)) / np.mean(normal_ce_0)
        
    return mr


def nmre(treatment, outcome, normal_dataset, strategic_dataset):

    # Estimate the causal effects assuming no confounding exists
    normal_1 = np.mean(normal_dataset[normal_dataset[treatment] == 1][outcome])
    normal_0 = np.mean(normal_dataset[normal_dataset[treatment] == 0][outcome])
    strategic_1 = np.mean(strategic_dataset[strategic_dataset[treatment] == 1][outcome])
    strategic_0 = np.mean(strategic_dataset[strategic_dataset[treatment] == 0][outcome])

    # Estimate the misreporting rate
    mr = ((normal_1 - normal_0) - (strategic_1 - strategic_0)) / (normal_1 - normal_0)

    return mr


def ndee(treatment, outcome, covariates, dataset):

    # Variables used by main model to predict the feature
    v = copy.deepcopy(covariates)
    v.append(treatment)
    
    # Obtain strategic split
    strategic_dataset = dataset[dataset['AGENT'] == 1]

    # Train the models
    model = XGBRegressor().fit(dataset[v], dataset[outcome])

    # Estimate the mr
    direct_effect = model.predict(strategic_dataset[covariates].assign(**{treatment: 1})[v]) \
                - model.predict(strategic_dataset[covariates].assign(**{treatment: 0})[v])    
    
    # Estimate the misreporting rate
    mr = np.mean(direct_effect) / np.mean(strategic_dataset[outcome])
    
    return mr


def ocsvm(normal_dataset, strategic_dataset):
    normal_dataset = normal_dataset.drop(columns='AGENT')
    normal_dataset = normal_dataset[normal_dataset['EMPLOYMENT'] == 1]
    strategic_dataset = strategic_dataset.drop(columns='AGENT')
    strategic_dataset = strategic_dataset[strategic_dataset['EMPLOYMENT'] == 1]
    clf = OneClassSVM(nu=0.01, kernel="rbf", gamma=0.1)
    clf.fit(normal_dataset)
    pred = clf.predict(strategic_dataset)
    mr = (np.sum(pred == -1) / len(strategic_dataset))
    return mr