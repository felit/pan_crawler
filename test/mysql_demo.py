import MySQLdb
conn = MySQLdb.connect(db='yunpan',host='localhost',user='root',passwd='admin')
cursor = conn.cursor()

cursor.execute('select * from yunpan.accounts')
result = cursor.fetchall()
print result


