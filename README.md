# Notifications Microservice
This is the repository for the notifications microservice. This microservice will handle email communication with customers and will likely be used for user communications. After further development it may be used for authentication.

API capabilities: This notification microservice will be responsible for communicating with indicated customers as required by the customers microservices. It is essentially an email server. It may be expanded in scope to encapsulate email authentication and user signup. It will have a database of past notifications and will have fields for timestamp, customerID, email address, and message.
- sendNotification(customerID)

# Get it running
The first time you want to get the application started you must enter the project's folder and specify the file you wish to run using the flask engine. Enter these command:
    pip install flask
    pip install Flask-Mail
    set FLASK_APP=notifications/app.py 

Then, whenever you want to get the microservice running, run this command:
    FLASK run

If you'd like to use GMail as your SMTP server then you'll be requird to lower the account security or you may be barred from sending emails usin the account you indicate.

# Example GET requests:
http://127.0.0.1:5000/api/notifications/all
http://127.0.0.1:5000/api/notifications?uid=123
http://127.0.0.1:5000/api/notifications?email=efosa@umass.edu