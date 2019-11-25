# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 09:15:08 2019

@author: Julie.Vranken
"""

import os

import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from azureml.core import Workspace



import mlflow
import mlflow.sklearn



def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

os.chdir("C:/Users/Julie.Vranken/Desktop/Data Science/MLflow_Houses")  
ws = Workspace.from_config()

mlflow.set_tracking_uri(ws.get_mlflow_tracking_uri())
experiment_name = 'experiment_mlflow_Houses'
mlflow.set_experiment(experiment_name)



if __name__ == "__main__":
    
    #Data loading 
    
 
    data = pd.read_csv("Train.csv",sep=",")
    
    #Search and replace missing values for certain columns
    
    data.isna().any()
      
    data.LotFrontage = data.LotFrontage.fillna(0)
    data.Alley = data.Alley.fillna("NoAlley")
    data.FireplaceQu = data.FireplaceQu.fillna("NoFP")
    data.GarageType = data.GarageType.fillna("NoGarage")
    data.GarageYrBlt = data.GarageYrBlt.fillna(0)
    data.GarageFinish = data.GarageFinish.fillna("NoGarage")
    data.GarageQual = data.GarageQual.fillna("NoGarage")
    data.GarageCond = data.GarageCond.fillna("NoGarage")
    data.PoolQC = data.PoolQC.fillna("NoPool")
    data.Fence = data.Fence.fillna("NoFence")
    data.MiscFeature = data.MiscFeature.fillna("None")
    
    #Remove remaining rows which contains a NA
    data = data.dropna()
   
                                         
    #transform the categorical columns using the sklearn OneHotEncoder. 
        
    list_cat = [2,5,6,7,8,9,10,11,12,13,14,15,16,21,22,23,24,25,27,28,29,30,31,32,33,35,39,40,41,42,53,55,57,58,60,63,64,65,72,73,74,78,79]
    list_num = [0,1,3,4,17,18,19,20,26,34,36,37,38,43,44,45,46,47,48,49,50,51,52,54,56,59,61,62,66,67,68,69,70,71,75,76,77,80]
    

    ct = ColumnTransformer([('oneHot',OneHotEncoder(categories='auto',sparse=False),list_cat)])
    ct_result = pd.DataFrame(ct.fit_transform(data))
    ct_result.columns = ct.get_feature_names()   
    
    ct_result.insert(0,"Id",ct_result.index+1)
    
    #merge categorical datafarme with numerical dataframe on ID
    #Store in processed full data dataframe
    
    numeric_df = data.iloc[:,list_num]
    p_full_data = pd.merge(ct_result,numeric_df, left_on='Id',right_on='Id',how='inner')
    
    list(p_full_data.columns)
    
    
    #Split data set in training and testing subset
  
    train, test = train_test_split(p_full_data)

    # The predicted column is "SalePrice"
    train_x = train.drop(["SalePrice"], axis=1)
    test_x = test.drop(["SalePrice"], axis=1)
    train_y = train[["SalePrice"]]
    test_y = test[["SalePrice"]]

    # set default values to parameters. By means of user input, we can deviate from it

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    
    
    

    
    
    
    # train model and include trade-off penalty parameters 

    with mlflow.start_run():
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)

        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_metric("alpha", alpha)
        mlflow.log_metric("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        
        mlflow.log_artifact("Houses_Model.py")

HTTPConnectionPool(host='40.71.86.251', port=5000): Max retries