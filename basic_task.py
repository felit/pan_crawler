# coding: utf8
import urllib2
import json
import sys

import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')
# 抓取过快问题
class BasicTask():
    def __init__(self):
        self.sleep_time_len = 90

        self.mysql_conn =MySQLdb.connect(db='yunpan', host='localhost', user='root', passwd='admin',charset="utf8")
        self.cursor = self.mysql_conn.cursor()

    def get_response(self, url, headers={}):
        response_json = None
        # TODO 错误处理，如果出错，延迟1分钟
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            response_json = response.read()
            # print url
            result = json.loads(response_json)
            return result
        except Exception as ex:
            print ex
            print response_json


"""
Traceback (most recent call last):
None
  File "/data/source/self/crawler_python/accounts_scheduler.py", line 22, in <module>
    scheduler.inter()
  File "/data/source/self/crawler_python/accounts_scheduler.py", line 17, in inter
    Accounts(account['follow_uk']).execute()
  File "/data/source/self/crawler_python/accounts.py", line 44, in execute
    self.get_first_task()
  File "/data/source/self/crawler_python/accounts.py", line 60, in get_first_task
    if(result.has_key('follow_list')):
AttributeError: 'NoneType' object has no attribute 'has_key'

"""