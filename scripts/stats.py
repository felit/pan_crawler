# coding: utf8
import MySQLdb
mysql_conn =MySQLdb.connect(db='yunpan', host='localhost', user='root', passwd='admin')
cursor = mysql_conn.cursor()
sql = """
    select count(*) from accounts
"""
cursor.execute(sql)
accounts_result = cursor.fetchall()
accounts_count = accounts_result[0][0]
sql = """
    select sum(pubshare_count) from accounts
"""
cursor.execute(sql)
share_count_result = cursor.fetchall()
share_count = share_count_result[0][0]
cursor.close()
mysql_conn.close()

print 'accounts num: %s ,pubshare_count num: %s' %(accounts_count, share_count)


