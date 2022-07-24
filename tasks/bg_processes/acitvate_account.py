''' Updates db to set user as active '''
import os
import mysql.connector


def activate_account(context):
    ''' finds '''
    try:
        cnx = mysql.connector.connect(user=os.environ['db_username'],
                                    password=os.environ['db_pass'],
                                    host='localhost',
                                    database='liaisesmart')

        with cnx.cursor() as cursor:
            query = (
                "UPDATE liaisesmart.user_login_details"
                "SET active = 1, activation_expiry = %s,"
                "activation_code = %s"
                "WHERE user_id = %s"
            )

            activation_expiry = context['activation_expiry']
            activation_code = context['activation_code']
            user_id = context['user_id']

            cursor.execute(query, (activation_expiry, activation_code, user_id))
            result = 1

    except mysql.connector.Error as err:
        print(f'Something went wrong {err}')
        result = 0
        return result

    return result
