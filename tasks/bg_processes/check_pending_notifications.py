''' Checks pending notifications '''
import os
import mysql.connector


def return_notifications():
    ''' Checks outstanding notifications and returns a dictionary of
    Pending notifications '''
    notifications = {}

    try:
        cnx = mysql.connector.connect(user=os.environ['db_username'],
                                      password=os.environ['db_pass'],
                                      host='localhost',
                                      database='liaisesmart')

        cursor = cnx.cursor()
        query = ("SELECT user_id, header, content FROM notifications"
                 "WHERE processed = 0")

        cursor.execute(query)

        for (user_id, header, content) in cursor:
            notifications[f'{user_id}'] = {
                'header': header, 'content': content}

        cursor.close()
        cnx.close()

    except mysql.connector.DatabaseError as db_err:
        print("Error connecting to the database {}").__format__(f'{db_err}')

    except mysql.connector.Error() as conn_err:
        print("error performing query {}").__format__(f'{conn_err}')

    return notifications
