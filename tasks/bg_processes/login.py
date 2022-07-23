''' Handles login requests
    To Do: create dict to return
'''
import os
from datetime import datetime, timedelta
import mysql.connector


def login(form):
    ''' Function to handle login requests '''
    try:
        cnx = mysql.connector.connect(user=os.environ['db_username'],
                                      password=os.environ['db_pass'],
                                      host='localhost',
                                      database='liaisesmart')

        with cnx.cursor() as cursor:
            query = ("SELECT u.user_id, u.user_type, t.descr, u.username,"
                     "aes_decrypt(u.enc_pw, %s) as 'password',"
                     "u.active, u.activation_code, u.activation_expiry,"
                     "u.dash_config, u.calendar_config,"
                     "u.locked, u.locked_until, u.two_fa, u.two_fa_mode,"
                     "u.two_fa_expiry, u.login_attempts, u.email_addr,"
                     "u.phone_num"
                     "FROM user_login_details u"
                     "INNER JOIN user_types t ON"
                     "t.user_type_id = user_type"
                     "WHERE u.username = %s")

            cursor.execute(
                query, (os.environ['db_encryption_key'], form.username))

            record = cursor.fetchone()

            # Checks if record has been found
            if record:
                # Loops over user record
                for (user_id, user_type, username, password,
                     active, activation_code, activation_expiry,
                     locked, locked_until, two_fa, two_fa_mode, two_fa_expiry,
                     login_attempts, email_addr, phone_num, dash_config,
                     calendar_config) in cursor:

                    date_format = '%Y-%m-%d %H:%M:%S'
                    locked_time = timedelta(minutes=10)

                    # checks if pw input matches pw in db
                    if password == form['password']:
                        # if account locked
                        if locked == 1:
                            # if locked but locked until time has passed
                            # update locked to 0
                            if datetime.now() > locked_until:
                                update_query = (
                                    "UPDATE user_login_details"
                                    "SET locked = 0"
                                    "WHERE user_id = %s"
                                )

                                cursor.execute(update_query, user_id)

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
                                    'phone_num': phone_num,
                                    'dash_config': dash_config,
                                    'calendar_config': calendar_config
                                }
                                # if user not active
                                if active != 1:
                                    context = {
                                        'user_details': user_details,
                                        'error': 'account not active'
                                    }
                                # if account active and not locked
                                else:
                                    context = {
                                        'user_details': user_details
                                    }
                            # add 10 mins to locked time and add error to
                            # user_details dict
                            else:
                                locked_until_time = datetime.strptime(
                                    locked_until, date_format)
                                new_time = locked_until_time + locked_time

                                update_query = (
                                    "UPDATE user_login_details"
                                    "SET locked_until = %s"
                                    "WHERE user_id = %s"
                                )
                                cursor.execute(update_query, (new_time, user_id))

                                context = {
                                    'user_details': {},
                                    'error': 'locked',
                                    'locked_until': new_time
                                }
                        # if account not locked
                        else:
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
                                    'phone_num': phone_num,
                                    'dash_config': dash_config,
                                    'calendar_config': calendar_config
                                }
                            if active != 1:
                                context = {
                                    'user_details': user_details,
                                    'error': 'account not active'
                                }
                            # if account active and not locked
                            else:
                                context = {
                                    'user_details': user_details
                                }
                    # if pw doesn't match
                    else:
                        # If account locked
                        if locked == 1:
                            # add 10 mins to locked time and add error to
                            # user_details dict
                            locked_until_time = datetime.strptime(
                                locked_until, date_format)
                            new_time = locked_until_time + locked_time

                            update_query = (
                                "UPDATE user_login_details"
                                "SET locked_until = %s"
                                "WHERE user_id = %s"
                            )
                            cursor.execute(update_query, (new_time, user_id))

                            context = {
                                'user_details': user_details,
                                'error': 'locked',
                                'locked_until': new_time
                            }
                        # if account not locked
                        else:
                            # add 1 to login attempts
                            new_attempt_no = login_attempts + 1
                            # if login attempts is more than / equal to 5
                            # lock account and update locked_until
                            if new_attempt_no >= 5:
                                the_date = datetime.now()
                                locked_until_time = the_date + locked_time

                                update_query = (
                                    "UPDATE user_login_details"
                                    "SET locked = 1,"
                                    "locked_until = %s,"
                                    "login_attempts = %s"
                                    "WHERE user_id = %s"
                                )

                                cursor.execute(
                                    update_query, (
                                            locked_until_time, new_attempt_no,
                                            user_id
                                        ))

                                user_details = {}

                                context = {
                                    'user_details': user_details,
                                    'error': 'locked',
                                    'locked_until': new_time
                                }
                            # if account not at max attempts
                            # add 1 to login attempts
                            else:
                                update_query = (
                                    "UPDATE user_login_details"
                                    "SET login_attempts = %s"
                                    "WHERE user_id = %s"
                                )

                                cursor.execute(
                                    update_query, (new_attempt_no, user_id))
                                user_details = {}
                                context = {
                                    'user_details': user_details,
                                    'error': 'incorrect login',
                                    'attempt': new_attempt_no
                                }
            # if record not found
            else:
                user_details = {}

                context = {
                    'user_details': user_details,
                    'error': 'incorrect login'
                }

        cnx.close()

    except mysql.connector.Error as err:
        user_details = {}
        context = {
                'error': err,
                'user_details': user_details
            }

        print(f'Something went wrong: {err}')

    return context
