
# Algemeen

Allereest dient er een Azure Machine Learning Workspace aangemaakt worden in Azure. Indien je deze creërt, wordt er automatisch een BLOB Storage aangemaakt waarin de artifacts van uitgevoerde runs worden bijgehouden. 

# Train et model en register parameters/metrieken van de correspondere runs

In de map ml_flow_azure_ml_workspace kan je de model_houses.py file terugvinden waarin de code beschreven staat om het huisprijzen model te trainen en informatie betreffende uitgevoerde runs weg te schrijven naar de Azure ML Workspace. 

Naast het oplijsten van de gebruikte libraries, definieren we eerst enkele metrieken die we willen gebruiken om ons model te evalueren.

```
def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2
```

Daarna haalt je jouw aangemaakte Workspace op en maakt een nieuw experiment aan (indien deze nog niet bestaat, merk op dat je dit ook rechstreeks in de ML workspace kan doen). Op deze manier kan je je runs weg schrijven naar een specifiek experiment in de ML workspace. Dit doen we door een config.json file te downloaden van de ML workspace in Azure en deze lokaal op te slaan in onze work directory. Deze config file bevat je subscription_id, resource_group en workspace_name in Azure (in jsnon formaat). 

```
ws = Workspace.from_config()
mlflow.set_tracking_uri(ws.get_mlflow_tracking_uri())
experiment_name = 'experiment_mlflow_Houses'
mlflow.set_experiment(experiment_name)
```
Daarna cleanen we onze data, trainen we het model en zetten we default waardes voor enkele parameters. 

```
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
```
Tot slot storten we een MLflow run en schrijven we bijhorende parameters/metrieken & artifacts weg naar de Azure ML worspace. Merk op dat in deze variant (in tegenstelling tot de VM variant, beschreven in ml_flow_azure_vm), het enkel nut heeft om de 'log_metric' (en niet ook log_param) functie te gebruiken aangezien enkel variabelen gelogd op deze manier gevisualeerd zullen worden in de Azure ML front-end. Indien je gedefineerde parameters dus wil registeren moet je dit ook doen via deze functie (en niet met een aparte functie log_param). Het nadeel hiervan is dat we front-end gewijs geen mooi onderscheid kunnen maken tussen beiden. 

```
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
```

# Registreer het 'beste' model, creëer hiervan een image en deploy dit als API

Bij het loggen van de artifacts wordt er in de BLOB storage van de ML workspace een conda.yaml, MLmodel en model.pkl file automatisch door MLflow aangemaakt. Deze folder mmoeten we eerst lokaal halen en kan je terugvinden in de artifacts folder van deze repository. 
Merk op dat we idealiter deze op Azure kunnen laten staan en niet lokaal moeten halen om dit te doen, maar dat wou nog niet lukken. 

Nu gaan we onze model registeren, een image creëeren en dit uiteindelijk deployen als API. De code hiervan kan je terugvinden in register_image_deploy.py. 

Hierin begin je met enkele constanten te definieren die info bevatten over de workspace op azure etc. Dit is eigenlijk hetzelfde als de config file die we voordien gebruikten (dus beiden opties zijn mogelijk voor deze stap):

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
model = Model.register(workspace=ws, model_path="./ml_flow_azure_ml_workspace/artifacts/model.pkl", model_name="house-model-gj")
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
                                 model_uri='./ml_flow_azure_ml_workspace/artifacts/',
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
