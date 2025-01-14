# Exercices Nikolas
Template for creating S3 bucket to trigger a simple state machine that copies the file into another S3 bucket


## Build & Deploy
```
sam validate --profile "formazione"
sam build --profile "formazione"
sam package --output-template-file packagedV1.yaml --s3-prefix REPOSITORY --s3-bucket formazione-staging --profile "formazione"
sam deploy --template-file .\packagedV1.yaml --stack-name Nik-SF-S3-CopyFile --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND --profile "formazione"
```


## Delete
  ```
  sam delete --stack-name Nik-SF-S3-CopyFile 
  ```