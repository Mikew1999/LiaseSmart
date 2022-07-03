''' Checks pending notifications '''
import os
import mysql.connector

cnx = mysql.connector.connect(user=os.environ['db_username'],
                              password=os.environ['db_pass'],
                              host='localhost',
                              database='liaisesmart')
