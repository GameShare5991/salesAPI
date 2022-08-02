# salesAPI
API gateway for performing CRD operations on GameShare sale data.

# build image: 
docker build . -t jackjackzhou/sales-api

# run image though docker: 
docker run --publish 4005:4005 sales-api

# push image:
docker push jackjackzhou/sales-api

# kubectl create&run
minikube start
kubectl create -f sales-app-deployment.yaml
minikube tunnel
minikube dashboard

# secret
kubectl create secret generic sales-app-key --from-file=serviceAccountKey.json

kubectl describe secrets/sales-app-key

# clean up
kubectl delete -f sales-app-deployment.yaml