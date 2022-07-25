import psycopg2 as pg
from getInfo import data
from config import user, db_name, password

try:
    conn = pg.connect(
        database=db_name,
        user=user,
        password=password)
except (Exception, pg.DatabaseError) as error:
    print(error)

cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE orders(
        id serial PRIMARY KEY,
        order_id INT,
        price_dollars,
        
    )

""")

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