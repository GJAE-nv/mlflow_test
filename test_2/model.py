WORKSPACE_NAME = "ml-flow-test"
SUBSCRIPTION_ID = "b242efdc-f14b-4f3e-a454-0377fa50302b"
RESOURCE_GROUP = "MLflow-analytics"
MODEL_NAME = "housing_model_gertjan_test"
IMAGE_NAME = "housing_model_gertjan_test-image"
EXPERIMENT_NAME = "housing_model_gertjan_test_experiment"
MODEL_PATH = "house_models_gertjan_path"
from azureml.core import Workspace, Model


ws = Workspace.get(name=WORKSPACE_NAME, subscription_id=SUBSCRIPTION_ID, resource_group=RESOURCE_GROUP)

model = Model.register(workspace=ws, model_path="./test_2/artifacts/model.pkl", model_name="house-model-gj")

model_path = Model.get_model_path('house-model-gj', _workspace=ws)

if __name__ == '__main__':
    print(model_path)
    print("ok")

############################################################################################

experiment_name = 'experiment_mlflow_Houses'
exp = ws.experiments[experiment_name]
runs = list(exp.get_runs())
# get the run ID and the path in run history
runid = runs[0].id

import mlflow.azureml
from azureml.core.webservice import AciWebservice, Webservice
# Build an Azure ML Container Image for an MLflow model
azure_image, azure_model = mlflow.azureml.build_image(
                                 model_uri='./test_2/artifacts/',
                                 workspace=ws,
                                 synchronous=True)

# If your image build failed, you can access build logs at the following URI:
print("Access the following URI for build logs: {}".format(azure_image.image_build_log_uri))

# Deploy the image to Azure Container Instances (ACI) for real-time serving
webservice_deployment_config = AciWebservice.deploy_configuration()
webservice = Webservice.deploy_from_image(
                    image=azure_image, workspace=ws, name="deploytestgertjan")
webservice.wait_for_deployment()





