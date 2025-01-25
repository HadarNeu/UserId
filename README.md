# UserId
User Data Retrieval Flask Application. 

#### Purpose:
- Fetches and filters JSON data from an external API
- Extracts and presents entries for a specific user ID
- Provides web endpoints for data access and visualization

#### Key Features:
- Dynamic user data filtering
- API JSON retrieval
- HTML-formatted data presentation
- Error handling for invalid user IDs

#### Endpoints:
- GET / : Home page
- GET /json : Full dataset retrieval
- GET /json/user/<user_id> : User-specific data display

## Deployment
The app can be deployed in any K8s deployment (EKS, GKE, AKS ...) since it's using a helm chart. 
For budget reasons I have created and tested my app in a local minikube cluster. 

## Whats Next? 
1. **Schema validation-** add schema validation to the code via [pydantic](https://pypi.org/project/pydantic/) package. 
2. **Cache-** implement cache for the get_json() function via [FlaskCaching](https://pypi.org/project/Flask-Caching/1.10.1/) package.
3. **Ingress controller-** add ingress controller. [IngressController](https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/)
4. **Implement Uplift -** uplift is a version management solution that can increase the version number in every PR/ commit to main. [Uplift](https://upliftci.dev/)

## So how can YOU use this app?
1. Choose a k8s distribution for the deployment of the app (EKS, minikube...)
2. Clone the repository (for the helm chart). 
3. Modify the ```./HelmChart/values.yaml``` file for your system's configuration. 
4. Helm install - you can use this command: 
```helm install user-id-app ./HelmChart --values ./HelmChart/values.yaml```
5. Optional: if you are using minikube, run this command to enable the NodePort service: 
```minikube service app-service```

You can now use the app on your bowser. 

