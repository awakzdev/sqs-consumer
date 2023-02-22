## Prerequisites 
It is required you have Keda installed on your cluster
```
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
kubectl create namespace keda
helm install keda kedacore/keda --namespace keda
```

## The following fields must be edited within values.yaml before running the chart.
```
image:
  repository: "foo" # Required. (You may upload the sqs-consumer to a registry and use the image with your own .env file)
  
secret:
  AWS_ACCESS_KEY_ID: "foo" # Required. please use plain text credentials, the helm chart will convert it to base64
  AWS_SECRET_ACCESS_KEY: "foo" # Required. please use plain text credentials, the helm chart will convert it to base64
  
scaledobject:
  scaleTargetRef:
    name: sqs-worker # name of deployment you wish to scale
  queueURL: # example url - "https://sqs.eu-central-1.amazonaws.com/946796614687/processing-queue"
  awsRegion: # example region - "eu-central-1"
```

## Installation
You must be in the helm directory
```
helm upgrade --install <chart-name> ./ -n <your-namespace> --create-namespace
```
