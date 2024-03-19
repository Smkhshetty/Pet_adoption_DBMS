import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='sooraj2008',
        database='PET_PROJ'
    )
