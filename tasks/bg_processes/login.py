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

        with cnx.cursor() as cursor:
            query = ("SELECT user_id, user_type, username,"
                     "aes_decrypt(enc_pw, %s) as 'password',"
                     "active, activation_code, activation_expiry,"
                     "locked, locked_until, two_fa, two_fa_mode,"
                     "two_fa_expiry, login_attempts, email_addr, phone_num"
                     "FROM user_login_details"
                     "WHERE username = %s")

            cursor.execute(
                query, (os.environ['db_encryption_key'], form.username))

            record = cursor.fetchone()

            if record:
                for (user_id, user_type, username, password,
                     active, activation_code, activation_expiry,
                     locked, locked_until, two_fa, two_fa_mode, two_fa_expiry,
                     login_attempts, email_addr, phone_num) in cursor:
                    if password == form['password']:
                        user_details = {
                            'user_id': user_id,
                            'username': username,
                            'password': password,
                            'user_type': user_type,
                            'active': active,
                            'activation_key': activation_code,
                            'activation_expiry': activation_expiry,
                            'locked': locked,
                            'locked_until': locked_until,
                            'two_fa': two_fa,
                            'two_fa_mode': two_fa_mode,
                            'two_fa_expiry': two_fa_expiry,
                            'login_attempts': login_attempts,
                            'email_addr': email_addr,
                            'phone_num': phone_num
                        }
                    else:
                        user_details = {}
            else:
                user_details = {}

        cnx.close()

    except mysql.connector.Error as err:
        user_details = {}
        print(f'Something went wrong: {err}')

    return user_details
