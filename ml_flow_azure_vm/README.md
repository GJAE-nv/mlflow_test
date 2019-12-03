# Algemene opmerking 

Deze README is uitgewerkt in Python. De R code kan teruggevonden worden in het corresponderende R script in deze repository. 

# Hoe MLflow op te zetten op een Virtual Machine 

## 1. Creëer een VM op Azure met de volgende specificaties: 
Microsoft Datacenter 2019: B2ms, Standard, General purpose, CPU 2, RAM 8, Datadisks 4, Max Iops 1920, Temp. Storage 16
- Verleen toegang tot HTTP, HTTPS, SSH and RDP in de configuratie van de VM
- Onthoud de username & password van de server (deze credentials heb je later nodig)

## 2. Connecteer met de VM door Microsoft Remote Desktop op te starten (op Windows is dit reeds geïnstalleerd, voor Mac ga je dit eerst nog moeten downloaden)
- Add PC:
    - <hostname: Public IP-Adress VM> : <RDP Port> (example: 52.137.9.17:3389)
- Connecteer met de server (username en password van set-up (stap 1))

## 3. Zodra de connectie tot stand gebracht is en je op de remote desktop bent, doorloop de volgende stappen:
- installeer python: navigeer naar de internet explorer https://www.python.org/downloads/release/
- open de command line in de server and typ het volgende om pip te installeren: 
```> curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```
```> python get-pip.py```
- installeer mlflow m.b.v. pip
```> pip install mlflow```

- start de mlflow server op VM
```> mlflow server host 0.0.0.0```

!mlflow server is now running on port 5000 on your VM.

## 4. Pas de firewall settings aan op de VM
- Navigeer naar de volgende directory: Control Panel\System and Security\Windows Defender Firewall
- Ga naar Advanced Settings -> Inbound Rules
- Voeg een nieuwe Inbound Rule toe: Port -> TCP -> specific local ports: 5000 (or all) -> ... 

## 5. Navigeer naar de Azure VM portal en voeg een Inbound port toe
- Voeg een inbound port toe en gebruik hiervoor port 5000. Verleen toegang tot 'any'

## 6. Check of je toegang hebt tot de de MLflow UI
Navigeer naar 'http://Public IP-Adress VM/5000' (example: http://52.137.9.17:5000/) url in jouw browser. 

# Train het model en registreer parameters/metrieken/artifacts van uitgevoerde runs

In de map ml_flow_azure_ml_vm kan je de model_houses.py file terugvinden waarin de code beschreven staat om het huisprijzen model te trainen en informatie betreffende uitgevoerde runs weg te schrijven naar de Azure ML Workspace. 

Naast het oplijsten van de gebruikte libraries, definieren we eerst enkele metrieken die we willen gebruiken om ons model te evalueren.

```
def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2
```

Om onze runs remotely te loggen, moeten we de MLFLOW_TRACKIN_URI environment variabele gelijkstellen aan de tracking server's URI. Hierbij gebruiken we de publieke IP van de opgezette server en de port 5000.

```
mlflow.tracking.set_tracking_uri("http://52.137.9.17:5000")

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
Tot slot starten we een MLflow run en schrijven we bijhorende parameters/metrieken & artifacts weg naar server. Merk op dat in deze variant (in tegenstelling tot de VM variant, beschreven in ml_flow_azure_vm) wel het onderscheid kunnen maken tussen parameters en metrieken.

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

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        
        mlflow.log_artifact("Houses_Model.py")
```




