#-*- coding:utf8 -*-
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
mysql_conn = MySQLdb.connect(db='yunpan', host='localhost', user='root', passwd='admin')
cursor = mysql_conn.cursor()


accounts_sql_tpl = """
INSERT INTO yunpan.accounts(
    follow_uk, fans_count, parent_follow_uk, avatar_url, pubshare_count, follow_uname, follow_count,
    user_type, intro, album_count, is_vip, type, follow_time,
     create_time, update_time, is_follow_crawler, is_files_crawler
) VALUES({follow_uk}, {fans_count}, '{parent_follow_uk}', '{avatar_url}', {pubshare_count},
        '{follow_uname}', {follow_count}, {user_type}, '{intro}', {album_count}, {is_vip}, {type}, '{follow_time}',
         '{create_time}', '{update_time}', {is_follow_crawler}, {is_files_crawler})
"""
import datetime, time, pymongo

conn = pymongo.MongoClient("127.0.0.1", 27017)
db = conn.accounts
for row in db.accounts.find({}):
    sql = accounts_sql_tpl.format(
        follow_uk=row['follow_uk'],
        fans_count=row['fans_count'],
        parent_follow_uk='%s' % row['parent_follow_uk'][0],
        avatar_url=row['avatar_url'],
        pubshare_count=row['pubshare_count'],
        follow_uname=row['follow_uname'].replace('\'','\\\''),
        follow_count=row['follow_count'],
        user_type=row['user_type'],
        intro=row['intro'].replace('\'','\\\''),
        album_count=row['album_count'],
        is_vip=row['is_vip'],
        type=row['type'],
        follow_time=time.strftime('%Y-%m-%d %H-%M-%S',time.gmtime(row['follow_time'])),
        create_time=datetime.datetime.today(),
        update_time=datetime.datetime.today(),
        is_follow_crawler=row['crawler'] if 'crawler' in row else False,
        is_files_crawler=False
    )
    # print sql
    try:
        cursor.execute(sql)
    except Exception, ex:
        print sql
        print Exception,":",ex
mysql_conn.commit()
cursor.close()
mysql_conn.close()