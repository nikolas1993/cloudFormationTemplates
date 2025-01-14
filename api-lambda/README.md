# Exercices Nikolas
Template for creating a simple API that calls a simple lambda function


## Build & Deploy
```
sam validate --profile "formazione"
sam build --profile "formazione"
sam package --output-template-file packagedV1.yaml --s3-prefix REPOSITORY --s3-bucket formazione-staging --profile "formazione"
sam deploy --template-file .\packagedV1.yaml --stack-name Nik-API-Lambda --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND --profile "formazione"
```


## Delete
  ```
  sam delete --stack-name Nik-API-Lambda 
  ```