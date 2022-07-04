''' Handles login requests
    To Do: create dict to return
'''
import os
import mysql.connector


def login(form):
    ''' Function to handle login requests '''
    cnx = mysql.connector.connect(user=os.environ['db_username'],
                                  password=os.environ['db_pass'],
                                  host='localhost',
                                  database='liaisesmart')

    cursor = cnx.cursor()

    query = ("SELECT user_id, user_type, username, aes_decrypt(enc_pw, %s) as 'password' FROM user_login_details"
             "WHERE username = %s")

    cursor.execute(query, (os.environ['db_encryption_key'], form.username))

    for user in cursor:
        print(
                f'User: {user.user_id}, user type: {user.user_type},'
                f'username: {user.username}, password: {user.password}'
            )

    cursor.close()
    cnx.close()

    return
