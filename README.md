# UserId
User Data Retrieval Flask Application. 

#### Purpose:
- Fetches and filters JSON data from an external API
- Extracts and presents entries for a specific user ID
- Provides web endpoints for data access and visualization

#### Key Features:
- Dynamic user data filtering
- RESTful JSON retrieval
- HTML-formatted data presentation
- Error handling for invalid user IDs

#### Endpoints:
- GET / : Home page
- GET /json : Full dataset retrieval
- GET /json/user/<user_id> : User-specific data display

## Deployment
The app is deployed locally using minikube and is installed via helm. 

## Challanges
1. No "merge" event so I had to use the push event. 
2. Data formatting - \n doesnt work in Flask. 
3. Docker limit for private images. Decided to make the image public. 
4. Image permissions, decided to use kubectl secrets to solve the issue. 

## Whats Next? 
1. make sure no one can push to main unless it's with an approved PR. 
2. Add schema validation to the code 
3. Add cache implementation to app 
4. Add ingress controller to the minikube deployment
5. Add version management tool called uplift 

## So how can YOU use this app?
Install minikube (a single node kubernetes tool). It's a great way for you to learn k8s and practice the skills in your home environment. Your'e going to need a docker engine installed as well. OR You can deploy this chart on your cloud kubernetes distribution. (Eks, Ecs etc.)

Clone the repository (for the helm chart)/ copy the helm chart and create your own values.yaml. 

Start the minikube cluster:

minikube start --driver=docker

Deploy the helm chart:
helm install user-id-app ./HelmChart --values ./HelmChart/values.yaml

Expose the NodePort service (skip this step if you are running the app on a k8s cloud dist.)
minikube service nginx-service

