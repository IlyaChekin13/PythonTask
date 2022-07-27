import psycopg2 as pg


db_name='taskdb'
user='ilyac'
password= '132731'

try:
    conn = pg.connect(
        database=db_name,
        user=user,
        password=password)
except (Exception, pg.DatabaseError) as error:
    print("Error while connecting database", error)

cursor = conn.cursor()


