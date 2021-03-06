# Notifications Microservice
Created by Christopher Gomez

This is the repository for the notifications microservice. This microservice will handle email communication with customers and will likely be used for user communications. After further development it may be used for authentication.

API capabilities: This notification microservice will be responsible for communicating with indicated customers as required by the customers microservices. It is essentially an email server. It may be expanded in scope to encapsulate email authentication and user signup. It will have a database of past notifications and will have fields for timestamp, customerID, email address, and message.

# Get it running
The first time you want to get the application started you must enter the project's folder, optionally initiate a virtual environment, and then run these commands to prepare usage of the flask framework.
    pip install flask
    set FLASK_APP=notifications/app.py 

Then, whenever you want to get the microservice running, run this command:
    FLASK run

Note that when assigning the credentials for the message to be sent that if you're going to use GMail then you'll likely be requird to lower the account security.

# API 
It is able to respond to GET requests that query for all notifications, all notifications from a specific email address, or all notifications from a specific customer id.
It is able to respond to POST requests (ideally from the Actors microservice) that ask for a message to be posted. The required arguments (in JSON form) are name, uid, message. It uses the parameters from the POST request to make a GET request to the Customers microservice to retrieve the email, which is then used to send the notification to the indicated email. It is then immediately stored in a database.

# Example GET requests:
http://127.0.0.1:5000/api/notifications/all
http://127.0.0.1:5000/api/notifications?uid=123
http://127.0.0.1:5000/api/notifications?email=efosa@umass.edu