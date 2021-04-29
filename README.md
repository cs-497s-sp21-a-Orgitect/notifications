# Notifications Microservice
This is the repository for the notifications microservice. This microservice will handle email communication with customers and will likely be used for user communications. After further development it may be used for authentication.

API capabilities: This notification microservice will be responsible for communicating with indicated customers as required by the customers microservices. It is essentially an email server. It may be expanded in scope to encapsulate email authentication and user signup. It will have a database of past notifications and will have fields for timestamp, customerID, email address, and message.
- sendNotification(customerID)