import psycopg2

dbname = "postgres"
user = "postgres"
password = ''
host = "localhost"


def getDBConnection():
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        print("Connected to the database!")
        return connection

    except psycopg2.Error as e:
        print("Unable to connect to the database.")
        print(e)
