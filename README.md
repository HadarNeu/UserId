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

## Whats Next? 
1. make sure no one can push to main unless it's with an approved PR. 

