import sqlite3, sys, datetime, traceback, flask, smtplib#, flask_mail
from flask import request, jsonify, Flask
# from flask_mail import Mail, Message
app = Flask(__name__)
app.config["DEBUG"] = True

# Mail server info. Will be used to send notification through email.
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yourId@gmail.com'       # Theoretically change this to your email address!
app.config['MAIL_PASSWORD'] = '*****'                  # Theoretically change this to your password!
app.config['MAIL_USE_TLS'] = False  # setting to true highly increases security
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
"""

# Creates the notifications database
def createTable():
    try:
        liteConnection = sqlite3.connect('notifications.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        creationCursor = liteConnection.cursor()
        
        # Table creation query string, executed through the cursor object that interacts with the sqLite database
        creation_query = "CREATE TABLE notifications (uid INTEGER, email VARCHAR(100), messages TEXT, time_sent TIMESTAMP);"
        creationCursor.execute(creation_query)
        print("Table created\n")

    except sqlite3.Error as errorMessage:
        print("Error while creating table,", errorMessage,"\n")

    # Close connection and cursor objects  
    finally:
        if liteConnection:
            liteConnection.close()

# Add new notifications to the database given the body info, recipient's user id, recipient email's address, and the date/time of sending
def addNotification(uid, email, message, time_sent):
    try:
        liteConnection = sqlite3.connect('notifications.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        # print("\nTotal changes: ", liteConnection.total_changes) # test connection

        # Cursor for sqLite interaction
        cursor = liteConnection.cursor()
        print("Cursor open, connected to SQLite")

        # Insert new notification object
        insertion_query = "INSERT INTO 'notifications' ('uid', 'email', 'messages', 'time_sent') VALUES (?, ?, ?, ?);"
        data_tuple = (uid, email, message, time_sent)
        cursor.execute(insertion_query, data_tuple)
        liteConnection.commit()
        print("Successfully commited new notification")

        # Make sure change went through by looking at all notifications. [Small data size]
        cursor.execute("SELECT * FROM notifications;")
        all_results = cursor.fetchall()
        print(all_results)

        # Close the cursor object
        cursor.close()

    except sqlite3.Error as errorMessage:
        print("Error while inserting new notification,", errorMessage)
        # print("\nException class is: ", errorMessage.__class__," \nException is", errorMessage.args)
        # print('Printing detailed SQLite exception traceback: ')
        # exc_type, exc_value, exc_tb = sys.exc_info()
        # print(traceback.format_exception(exc_type, exc_value, exc_tb))
    
    # close connection/cursor 
    finally:
        if liteConnection:
            liteConnection.close()

# "Main Page" of Microservice. Essentially a pretty placeholder.
@app.route('/', methods=['GET'])
def home():
    return "<h1>Notification Microservice</h1><p>This site is a prototype API for the Notifications microservice of project Orgitect.</p>"


# Handles showing all of the notifications in the database. Impractical, but useful for testing.
@app.route('/api/notifications/all', methods=['GET'])
def api_all():
    try:
        liteConnection = sqlite3.connect('notifications.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        getCursor = liteConnection.cursor()
        all_notifications = getCursor.execute('SELECT * FROM notifications;').fetchall()
        # TO-DO: Include try-catch. Make sure to CLOSE the liteConnection.
        if liteConnection:
            liteConnection.close()
        return jsonify(all_notifications)

    except sqlite3.Error as errorMessage:
        print("Error while getting ALL notifications,", errorMessage)

    # close connection/cursor 
    finally:
        if liteConnection:
            liteConnection.close()

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>ERROR 404</h1><p>Sorry, what you have requested could not be found.</p>", 404


@app.route('/api/notifications', methods=['GET'])
def api_filter():
    try:
        # retrieve indicated query parameters from the URL
        query_params = request.args
        uid = query_params.get('uid')
        email = query_params.get('email')

        query = "SELECT * FROM notifications WHERE"
        filters = []

        # Check which filters it has, or throw an error if none.
        if uid:
            query += ' uid=? AND'
            filters.append(uid)
        if email:
            query += ' email=? AND'
            filters.append(email)
        if not (id or email):
            return page_not_found(404)
        query = query[:-4] + ';'    # get rid of the potential trailing AND, end with semicolon to fulfill sqLite format.

        # Run indicated query on the object that interacts with sqLite and return the JSON format of results found.
        liteConnection = sqlite3.connect('notifications.db')
        queryCursor = liteConnection.cursor()
        results = queryCursor.execute(query, filters).fetchall()
        return jsonify(results)

    except sqlite3.Error as errorMessage:
        print("Error while getting FILTERED notifications,", errorMessage)

    # close connection/cursor 
    finally:
        if liteConnection:
            liteConnection.close()

# Receive Post request from the Actors microservice (Yidan) here
@app.route('/api/notifications', methods=['POST'])
def addNewNotificiation():
    try:
        # break the JSON file down into necessary values
        request_data = request.get_json()
        name = request_data['name'] # Email address holder's name
        uid = request_data['uid']   # Email address holder's unique customer ID
        message = request_data['message']   # Message to be sent to Email address holder
        time_sent = datetime.datetime.now() # Time of send request
        
        # Make get request to the Customers microservice (Efosa) here
        url = 'localhost:3000/api/notification'
        params = uid    # The only parameter to be passed in is the customer ID, aka uid
        email = request.get(url, { params })

        # Send notification/email via Flask
        """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        flaskMsg = Message('Hello', sender = 'yourId@gmail.com', recipients = [email])
        flaskMsg.body = message
        mail.send(flaskMsg)
        """

        # Add email details to the  notifications database via the addNotification() function
        addNotification(uid, email, message, time_sent)

    except sqlite3.Error as errorMessage:
        print("Error while getting sending notification,", errorMessage)

"""
# Dummy Data
createTable()
addNotification(453, 'efosa@umass.edu', 'Hey cutie call me at 1-800-CARS-FOR-KIDS', datetime.datetime.now())
addNotification(123, 'chris@umass.edu', 'Big black hole, long black hair, WWWWWAAAAA', datetime.datetime.now())
addNotification(453, 'efosa@umass.edu', 'I bet you still play Runescape', datetime.datetime.now())
addNotification(453, 'efosa@umass.edu', 'Do you kiss your mother with that mouth?', datetime.datetime.now())
"""