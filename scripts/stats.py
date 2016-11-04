# coding: utf8
import MySQLdb
mysql_conn =MySQLdb.connect(db='yunpan', host='localhost', user='root', passwd='admin')
cursor = mysql_conn.cursor()
sql = """
    select count(*) from accounts
"""
cursor.execute(sql)
result = cursor.fetchall()
print result