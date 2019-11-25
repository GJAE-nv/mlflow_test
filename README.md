# MLflow on Azure ML workspace & MLflow on Azure Virtual Machine

In deze repository kan je informatie terugvinden betreffende het tracken & deployen van een ML model via het open source platform MLflow  op Azure. 

Meer specifiek kan je een handleiding terugvinden betreffende volgende 2 toepassingen:
  - Hoe een connectie maken tussen de MLflow library & een Azure Machine Learning Workspace (ml_flow_azure_ml_workspace)? 
  - Hoe een mlflow server opzetten op een Azure Virtual Machine (VM) (ml_flow_azure_vm)).?
  
In elke directory is er een README toegevoegd met verdere uitleg over beiden luiken. 

In dit voorbeeld maken we gebruik van een python model om huisprijzen te voorspellen. 

## The data

De data die gebruikt wordt om dit model te trainen kan je terugvinden in 'Train.csv'

## The model

De python code voor het trainen van het model en het tracken van de parameters en/of metrieken van de bijhorende runs kan je terugvinden in de model.py file in beide directories. 

Merk op dat afhankelijk van de gekozen toepassing (ml_flow_ml_workspace of ml_flow_azure_vm), deze code lichtjes zal verschillen, aangezien de runs naar een andere plaats geschreven worden (dit is duidelijk aangegeven in de bijhorend README). 

## Artifact download

In deze directory vindt je 2 python scripts terug om de gecreëerde artifacts door MLflow in de Azure Blob Storage te downloaden:
  - artifact_container_download.py: verschaft ons de mogelijkheid om alle artifacten van een bepaalde Azure Blog Storage container te downloaden. 
  - artifcat_experiment_download.py: verschaft ons de mogelijkheid om enkel de artifacten betreffende eenspecifeke run te downloaden.

Deze artifacten hebben we locaal nodig om nadien een model te creëren in de Azure Machine Learning Worspace. 

Merk op dat we idealiter deze stap kunnen overslaan door rechtstreeks de artifacten in de Blob Storage te gebruiken in plaats van deze eerst lokaal binnen te halen. Dit is ons echter nog niet gelukt!

Enjoy!
--------------------------------------------------------------
Julie & Gertjan 

Note: Het is aan te raden om eerst de documentatie betreffende de basisconcepten van 'mlflow' onder de loep te nemen, alvorens effectief aan de slag te gaan. Dit kan je terugvinden via de volgende link:  https://mlflow.org/docs/latest/index.html.
