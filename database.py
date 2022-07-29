import psycopg2 as pg


class Database:

    def __init__(self):
        db_name='taskdb'
        user='ilyac'
        password= '132731'
        
        
        self.conn = pg.connect(
            database=db_name,
            user=user,
            password=password)

        self.conn.autocommit = False
        self.cur = self.conn.cursor()
        # check existing of the table
        try:
            self.create_table()
        except Exception as error:
            print("table already exists")
            self.conn.rollback()
            # if there is a table
            self.cur.execute(f"""DROP TABLE "data" """)
            self.create_table()

    
    def create_table(self):
        """create db table"""
        self.cur.execute(f"""CREATE TABLE "data"
                                        ("№" INTEGER PRIMARY KEY,
                                        "Заказ №" INTEGER,
                                        "Стоимость, $" REAL,
                                        "Стоимость, RUB" REAL,
                                        "Срок поставки" DATE)""")
        self.conn.commit()

    # Обновление таблицы
    def update_table(self, data):
        for i in range(1, len(data)):
            date =  data[i][4][-4:] + "-" + data[i][4][3:5] + "-" + data[i][4][:2]
            self.cur.execute(f"""SELECT * FROM "data" WHERE "№" = {int(data[i][0])}""")
            # Если есть такая запись (обновление)
            if self.cur.fetchone():
                self.cur.execute(f"""UPDATE "data" 
                                     SET "Заказ №"={int(data[i][1])},
                                         "Стоимость, $"={float(data[i][2])},
                                         "Стоимость, RUB"={float(data[i][3])},
                                         "Срок поставки"='{date}' 
                                     WHERE "№"={int(data[i][0])} """)
                self.conn.commit()
            # Если записи нет (добавление)
            else:
                self.cur.execute(f"""INSERT INTO "data" 
                                     ("№", "Заказ №", "Стоимость, $", "Стоимость, RUB", "Срок поставки")
                                     VALUES (
                                     {int(data[i][0])}, 
                                     {int(data[i][1])}, 
                                     {float(data[i][2])}, 
                                     {float(data[i][3])},
                                     '{date}')""")
                self.conn.commit()

    # Обновление таблицы
    def update_with_delete(self, data):
        self.cur.execute(f"""DELETE FROM "data" """)
        self.update_table(data)