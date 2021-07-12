import os
import shutil
import sqlite3
shutil.rmtree('frame')
os.mkdir('frame')
conn = sqlite3.connect("people_num.db")
cur = conn.cursor()
sql = '''
    delete from "num";
'''
cur.execute(sql)
conn.commit()

cur.close()
conn.close()