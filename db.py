import psycopg2 as pg
from getInfo import data
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


tmp_df = "tmp_dataframe.csv"
data.to_csv(tmp_df, index_label='id', header=False)
f = open(tmp_df, 'r')

try:
    cursor.copy_from(f, db_name, sep=",")
    conn.commit()
except (Exception, pg.DatabaseError) as error:
    print(error)
    conn.rollback()
    cursor.close()

cursor.close()
conn.close()