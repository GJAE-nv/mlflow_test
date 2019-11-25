# MLflow on Azure ML workspace and/or Azure Virtal Machine

In the following repository you'll find a way to make a connection between the mlflow library and and Azure Machine Learning Workspace (ml_flow_azure_ml_workspace) & you can find a way to setup a mlflow server on an Azure Virtual Machine (ml_flow_azure_vm). In each directory you'll find a README.

In this example we'll use a model to predict Housing Prices

## The Data
The data used for this Machine Learning Model is stored in Train.csv

## The model
The model to predict the House Prices is stored in the Houses_model.py file

## Artifact download
In this directory you'll find two python scripts to download the artifacts created by mlflow frm the Azure Blob storage. 
The artifact_experiment_download.py makes it possible to download only the artifacts for one specific run. You'll need these
artifacts to create your model in Azure Machine Learning Workspace

Enjoy!
--------------------------------------------------------------
Julie & Gertjan 

