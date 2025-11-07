import copy
from xgboost import XGBRegressor
import numpy as np
from sklearn.model_selection import train_test_split

# accounts for confounder U
def cmre_ds(X, outcome, covariates, TM_data, MA_data):
    # X = treatment (in Medicare example, this is the reported value of employement)

    # Variables used by main model to predict anchor
    v = copy.deepcopy(covariates)
    v.append(X)
    
    train_MA_data, test_MA_data = train_test_split(MA_data, test_size=0.2, random_state=42)

    # Split the MA dataset and the normal dataset
    train_MA_data_0 = train_MA_data[train_MA_data[X] == 0] # clean MA dataset
    train_TM_data_1 = TM_data[TM_data[X] == 1]  # clean TM dataset

    test_MA_data_1 = test_MA_data[test_MA_data[X] == 1]
    test_MA_data_0 = test_MA_data[test_MA_data[X] == 0]

    # Train the models using the train split
    clean_MA_predictor = XGBRegressor().fit(train_MA_data_0[covariates], train_MA_data_0[outcome])
    clean_TM_predictor = XGBRegressor().fit(train_TM_data_1[covariates], train_TM_data_1[outcome])
    all_MA_predictor = XGBRegressor().fit(train_MA_data[v], train_MA_data[outcome])

    # Estimate the CATEs
    MA_ce_1 = all_MA_predictor.predict(test_MA_data_1[covariates].assign(**{X: 1})[v]) \
                - all_MA_predictor.predict(test_MA_data_1[covariates].assign(**{X: 0})[v])    # T_a
    TM_ce_1 = clean_TM_predictor.predict(test_MA_data_1[covariates]) \
                - clean_MA_predictor.predict(test_MA_data_1[covariates]) # T'_a
    TM_ce_0 = clean_TM_predictor.predict(test_MA_data_0[covariates]) \
                - clean_MA_predictor.predict(test_MA_data_0[covariates]) # delta'_a
    
    # Estimate the misreporting rate
    mr = (np.mean(TM_ce_1) - np.mean(MA_ce_1)) / np.mean(TM_ce_0)
        
    return mr

def cmre_ds_adjusted_for_U(X, outcome, covariates, TM_data, MA_data, U):
    # X = treatment (in Medicare example, this is the reported value of employement)
    # Y = outcome
    # this function assumes U is binary and can take on the values {0, 1}

    # Variables used by main model to predict anchor
    v = copy.deepcopy(covariates)
    v.append(X)

    extended_variables = copy.deepcopy(covariates)
    extended_variables.append(U)
    
    train_MA_data, test_MA_data = train_test_split(MA_data, test_size=0.2, random_state=42)

    # Split the MA dataset and the normal dataset
    TM_data_1 = TM_data[TM_data[X] == 1]  # clean TM dataset

    test_MA_data_1 = test_MA_data[test_MA_data[X] == 1]
    test_MA_data_0 = test_MA_data[test_MA_data[X] == 0]

    # Train the models using the train split
    MA_predictor = XGBRegressor().fit(train_MA_data[v], train_MA_data[outcome])
    clean_TM_extended_predictor = XGBRegressor().fit(TM_data_1[extended_variables], TM_data_1[outcome])
    MA_U_predictor = XGBRegressor().fit(train_MA_data[covariates], train_MA_data[U])

    # Estimate the CATEs
    MA_ce_1 = MA_predictor.predict(test_MA_data_1[covariates].assign(**{X: 1})[v]) \
                - MA_predictor.predict(test_MA_data_1[covariates].assign(**{X: 0})[v])    # T_a
    TM_ce_1 = clean_TM_extended_predictor.predict(test_MA_data_1[covariates].assign(**{U: 1})[extended_variables]) * MA_U_predictor.predict(test_MA_data_1[covariates]) \
                + clean_TM_extended_predictor.predict(test_MA_data_1[covariates].assign(**{U: 0})[extended_variables]) * (1 - MA_U_predictor.predict(test_MA_data_1[covariates])) \
                - MA_predictor.predict(test_MA_data_1[covariates].assign(**{X: 0})[v]) # T'_a
    # Muskaan: Not sure about how I've translated the T'_a and delta'_a formulae into code
    TM_ce_0 = clean_TM_extended_predictor.predict(test_MA_data_0[covariates].assign(**{U: 1})[extended_variables]) * MA_U_predictor.predict(test_MA_data_0[covariates]) \
                + clean_TM_extended_predictor.predict(test_MA_data_0[covariates].assign(**{U: 0})[extended_variables]) * (1 - MA_U_predictor.predict(test_MA_data_0[covariates])) \
                - MA_predictor.predict(test_MA_data_0[covariates].assign(**{X: 0})[v]) # delta'_a
    
    # Estimate the misreporting rate
    mr = (np.mean(TM_ce_1) - np.mean(MA_ce_1)) / np.mean(TM_ce_0)
        
    return mr


# version of the function with old variable names:

# def cmre_ds(treatment, outcome, covariates, normal_dataset, strategic_dataset):

#     # Variables used by main model to predict anchor
#     v = copy.deepcopy(covariates)
#     v.append(treatment)
    
#     train_strategic_df, test_strategic_df = train_test_split(strategic_dataset, test_size=0.2, random_state=42)

#     # Split the strategic dataset and the normal dataset
#     train_strategic_df_0 = train_strategic_df[train_strategic_df[treatment] == 0] # clean MA dataset
#     train_normal_df_1 = normal_dataset[normal_dataset[treatment] == 1]  # clean TM dataset

#     test_strategic_df_1 = test_strategic_df[test_strategic_df[treatment] == 1]
#     test_strategic_df_0 = test_strategic_df[test_strategic_df[treatment] == 0]

#     # Train the models using the train split
#     clean_MA_predictor = XGBRegressor().fit(train_strategic_df_0[covariates], train_strategic_df_0[outcome])
#     clean_TM_predictor = XGBRegressor().fit(train_normal_df_1[covariates], train_normal_df_1[outcome])
#     all_MA_predictor = XGBRegressor().fit(train_strategic_df[v], train_strategic_df[outcome])

#     # Estimate the CATEs
#     normal_ce_1 = clean_TM_predictor.predict(test_strategic_df_1[covariates]) \
#                 - clean_MA_predictor.predict(test_strategic_df_1[covariates]) # T'_a
#     normal_ce_0 = clean_TM_predictor.predict(test_strategic_df_0[covariates]) \
#                 - clean_MA_predictor.predict(test_strategic_df_0[covariates]) # delta'_a
#     strategic_ce_1 = all_MA_predictor.predict(test_strategic_df_1[covariates].assign(**{treatment: 1})[v]) \
#                 - all_MA_predictor.predict(test_strategic_df_1[covariates].assign(**{treatment: 0})[v])    # T_a
    
#     # Estimate the misreporting rate
#     mr = (np.mean(normal_ce_1) - np.mean(strategic_ce_1)) / np.mean(normal_ce_0)
        
#     return mr