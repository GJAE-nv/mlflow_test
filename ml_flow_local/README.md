# Track experiments locally with MLflow 

In deze repisotory kan je een python & R script terugvinden die je toelaten om een model lokaal te trainen en vervolgens parameters, metrieken & artificats te runnen van uitgevoerde runs binnen een bepaald experiment. 

Het R & Python script hebben de volgende opbouw: 
- Installeren van nodige packages 
- Het zetten van de tracking URI naar onze local host (optioneel, want dit gebeurt achterliggend automatisch indien niet anders gespecifieerd)
- Data inladen & data cleanen
- Het definiëren van parameters met default values
- Het aanmaken van een experiment 
- Het tracken van parameters, metrieken & artifacts van een run binnen dit aangemaakte experiment 

Indien het script wordt uitgevoerd via de CML, kan je ook andere waardes meegeven voor de parameters dan de defaults die gedefinieerd worden in het script. 

Nadien kan je via het command 'MLflow server' in de CLI een lokale server opzetten. De Traking server UI kan je dan raadplegen door in je browser te navigeren naar je local host (http://127.0.0.1:5000).
