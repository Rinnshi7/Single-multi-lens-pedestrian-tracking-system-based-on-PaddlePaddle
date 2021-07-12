import sqlite3

conn = sqlite3.connect("people_num.db")

c = conn.cursor()

# sql = '''
#         create table num
#         (num int not null);
# '''
# c.execute(sql)

num = conn.execute("SELECT * from  num where rowid == 10")
for i in num:
    a = i[0]
    print(a)
conn.commit()
conn.close()

print("OPEN SUCCESSFULLY")