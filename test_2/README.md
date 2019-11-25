# ML flow and Azure Machine Learning Workspace 

In de map test_2 heb je een model.py file en een artifacts folder waar je de conda.yaml, MLmodel en model.pkl terugvindt. Deze laatste drie zijn dus de files die mlflow voor ons aanmaakt. Het zou mooi zijn als we die gewoon op Azure kunnen laten staan en niet lokaal moeten halen om dit te doen, maar dat wou nog niet lukken. 

In model.py begin je met enkele constanten te definieren die info bevatten over de workspace op azure etc. Dit is eigenlijk hetzelfde als de config file die we voordien gebruikte:

```
WORKSPACE_NAME = "ml-flow-test"
SUBSCRIPTION_ID = "b242efdc-f14b-4f3e-a454-0377fa50302b"
RESOURCE_GROUP = "MLflow-analytics"
MODEL_NAME = "housing_model_gertjan_test"
IMAGE_NAME = "housing_model_gertjan_test-image"
EXPERIMENT_NAME = "housing_model_gertjan_test_experiment"
MODEL_PATH = "house_models_gertjan_path"
```

Je haalt je workspace hierna terug op en je steekt het in de variabele 'ws':

```from azureml.core import Workspace, Model
ws = Workspace.get(name=WORKSPACE_NAME, subscription_id=SUBSCRIPTION_ID, resource_group=RESOURCE_GROUP)
```

Hierna ga je je model gaan registreren in de workspace. Dit komt dan mooi in je Model submenu. Je gebruikt hier de module ML van azureml.core. Dus vergeet zeker niet beide Workspace en Model hiervan te importeren. het model_path is hier een relative path naar je pickle file in de artifacts folder. Het zou dus op termijn mooi zijn als we dit kunnen linken met onze BLOB storage.

```
from azureml.core import Workspace, Model
model = Model.register(workspace=ws, model_path="./test_2/artifacts/model.pkl", model_name="house-model-gj")
```

De volgende code lines zijn puur ter bevestiging van of het gelukt is en je wat info terug te geven:

```
model_path = Model.get_model_path('house-model-gj', _workspace=ws)
if __name__ == '__main__':
    print(model_path)
    print("ok")
```
Nu we ons model hebben kunnen we hier een image van gaan maken. Je kan deze image zien als Docker file. Dit gaat dan ook wat tijd kosten. Je kan deze image ook in de Azure interface zelf maken. Hier ga je het gewoon aanroepen vie Python. De 'build_image' module van mlflow.azureml verwacht ook de model_uri, maar deze moet dus de gehele artifacts folder zijn. 
```
import mlflow.azureml
from azureml.core.webservice import AciWebservice, Webservice
# Build an Azure ML Container Image for an MLflow model
azure_image, azure_model = mlflow.azureml.build_image(
                                 model_uri='./test_2/artifacts/',
                                 workspace=ws,
                                 synchronous=True)
# If your image build failed, you can access build logs at the following URI:
print("Access the following URI for build logs: {}".format(azure_image.image_build_log_uri))
```
Als laatste willen we het model gaan deployen als API. Je gaat de 'deploy_from_image' gebruiken om dus je image die je zonet hebt gemaakt te gaan deployen. Hierna kan krijg je een url dat de api moet voorstellen. Deze kan je dan gaan aanspreken via POSTMAN. 
```
# Deploy the image to Azure Container Instances (ACI) for real-time serving
webservice_deployment_config = AciWebservice.deploy_configuration()
webservice = Webservice.deploy_from_image(
                    image=azure_image, workspace=ws, name="deploytestgertjan")
webservice.wait_for_deployment()
```
NOTE: Het builden van een image en deployen kan even duren... :-)
