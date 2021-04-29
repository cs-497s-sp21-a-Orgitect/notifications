import sqlite3
import datetime
import sys
import traceback

def createTable():
    try:
        # print("Creating table process")
        # liteConnection = sqlite3.connect(":memory:")    # exists strictly in memory, not in a file
        liteConnection = sqlite3.connect('notifications.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        # print("Total changes", liteConnection.total_changes) # test connection

        # Cursor for sqLite interaction
        creationCursor = liteConnection.cursor()    # might swap to sqliteConnection.cursor()
        
        # Table creation query
        creation_query = "CREATE TABLE notifications (uid INTEGER, email VARCHAR(100), messages TEXT, time_sent TIMESTAMP);"
        creationCursor.execute(creation_query)
        print("Table created\n")

    except sqlite3.Error as errorMessage:
        print("Error while creating table,", errorMessage,"\n")
        
    finally:    # """Close cursor & connection objects."""
        if liteConnection:
            liteConnection.close()


# TO-DO: Make immune to injection attacks using ? ? ? 
def addNotification(uid, email, message, time_sent): # TO-DO: rename datetime to timestamp, follow through changes
    try:
        liteConnection = sqlite3.connect('notifications.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        print("\nTotal changes: ", liteConnection.total_changes) # test connection

        # Cursor for sqLite interaction
        cursor = liteConnection.cursor()    # might swap to sqliteConnection.cursor()
        print("Cursor open, connected to SQLite")
        
        # Table creation query
        # creation_query = "CREATE TABLE notifications (uid INTEGER, email TEXT, messages TEXT, time_sent TIMESTAMP);" 
        # cursor.execute(creation_query)

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
    
    finally:    # """Close cursor & connection objects."""
        if liteConnection:
            liteConnection.close()
            # rows = cursor.execute("SELECT 1").fetchall()    # Test they are closed by a statement that should return 1. TO-DO: Verify fluency.
            # print(rows)

createTable()
addNotification(453, 'efosa@umass.edu', 'Hey cutie call me at 1-800-CARS-FOR-KIDS', datetime.datetime.now())
addNotification(123, 'chris@umass.edu', 'Big black hole, long black hair, WWWWWAAAAA', datetime.datetime.now())
addNotification(453, 'efosa@umass.edu', 'I bet you still play Runescape', datetime.datetime.now())
addNotification(453, 'efosa@umass.edu', 'Do you kiss your mother with that mouth?', datetime.datetime.now())

""" ~~~~~~~~~~~~~~~~~~~~~~~~ Searching for a specific "Fish" name ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
target_fish_name = "Jamie"
rows = cursor.execute(
    "SELECT name, species, tank_number FROM fish WHERE name = ?",
    (target_fish_name,),
).fetchall()
print(rows)
"""

""" ~~~ Searching for an indicated number of users with a specific name ~~~~~~~~~~~~~~~~~~~~~~
cur.execute("SELECT * FROM users;")
three_results = cur.fetchmany(3)
print(three_results)
"""

""" ~~~~~~~~~~~~ Making sure a change went through by looking at all fishes ~~~~~~~~~~~~~~~~~
rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)
"""

""" Edit later to reflect more functional database, similar to this just pythonified
CREATE TABLE Car
(
Pk_Car_Id INT PRIMARY KEY,
Brand VARCHAR(100),
Model VARCHAR(100)
);

CREATE TABLE Engineer
(
Pk_Engineer_Id INT PRIMARY KEY,
FullName VARCHAR(100),
MobileNo CHAR(11),
Fk_Car_Id INT FOREIGN KEY REFERENCES Car(Pk_Car_Id)
);

# cursor.execute("CREATE TABLE customerdb (uid INTEGER, email TEXT)")
# cursor.execute("messages TEXT, timestamp INTEGER)")
"""