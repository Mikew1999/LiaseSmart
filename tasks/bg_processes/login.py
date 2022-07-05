''' Handles login requests
    To Do: create dict to return
'''
import os
import mysql.connector


def login(form):
    ''' Function to handle login requests '''
    try:
        cnx = mysql.connector.connect(user=os.environ['db_username'],
                                      password=os.environ['db_pass'],
                                      host='localhost',
                                      database='liaisesmart')

        cursor = cnx.cursor()

        query = ("SELECT user_id, user_type, username,"
                 "aes_decrypt(enc_pw, %s) as 'password'"
                 "FROM user_login_details"
                 "WHERE username = %s")

        cursor.execute(query, (os.environ['db_encryption_key'], form.username))

        for user in cursor:
            user_details = {
                'user_id': user.user_id,
                'username': user.username,
                'password': user.password,
                'user_type': user.user_type
            }

        cursor.close()
        cnx.close()

    except mysql.connector.Error as err:
        user_details = {}
        print(f'Something went wrong: {err}')

    return user_details
