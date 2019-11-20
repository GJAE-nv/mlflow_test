WORKSPACE_NAME = "ml-flow-test"
SUBSCRIPTION_ID = "b242efdc-f14b-4f3e-a454-0377fa50302b"
RESOURCE_GROUP = "MLflow-analytics"
MODEL_NAME = "housing_model_gertjan_test"
IMAGE_NAME = "housing_model_gertjan_test-image"
EXPERIMENT_NAME = "housing_model_gertjan_test_experiment"
MODEL_PATH = "house_models_gertjan_path"
from azureml.core import Workspace
# workspace.py
def get_workspace():
 	ws = Workspace.get(name=WORKSPACE_NAME, subscription_id=SUBSCRIPTION_ID, resource_group=RESOURCE_GROUP)
 	return ws