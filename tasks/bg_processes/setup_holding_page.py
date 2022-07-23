''' Sets up holding page '''
import os
import mysql.connector


# def setup_dash(dash_id, user_id):
#     ''' Queries db to find dash config '''
#     try:
#         cnx = mysql.connector.connect(user=os.environ['db_username'],
#                                       password=os.environ['db_pass'],
#                                       host='localhost',
#                                       database='liaisesmart')

#         with cnx.cursor() as cursor:
#             query = (
#                 "SELECT * FROM dash_config"
#                 "WHERE dash_id = %s"
#                 )
#             cursor.execute(
#                 query, (dash_id))

#     ret
