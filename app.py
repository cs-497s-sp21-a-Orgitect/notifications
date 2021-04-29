# Note, to run this flask file first:
# set FLASK_APP=notifications/app.py
# FLASK run
# Example query searches.
# http://127.0.0.1:5000/api/notifications/all
# http://127.0.0.1:5000/api/notifications?uid=123
# http://127.0.0.1:5000/api/notifications?email=efosa@umass.edu
import flask, sqlite3
from flask import request, jsonify, Flask
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Notification Microservice</h1><p>This site is a prototype API for the notification microservice of projet 'Orgitect'.</p>"


@app.route('/api/notifications/all', methods=['GET'])
def api_all():
    liteConnection = sqlite3.connect('notifications.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    getCursor = liteConnection.cursor()
    all_notifications = getCursor.execute('SELECT * FROM notifications;').fetchall()
    # TO-DO: Include try-catch. Make sure to CLOSE the liteConnection.
    if liteConnection:
        liteConnection.close()
    return jsonify(all_notifications)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>ERROR 404</h1><p>Sorry, what you have requested could not be found.</p>", 404


@app.route('/api/notifications', methods=['GET'])
def api_filter():
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

# app.run()   # can put in a main at the end if needed. Silently ignored otherwise.