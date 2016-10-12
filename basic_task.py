# coding: utf8
import urllib2
import json
import pymongo
# 抓取过快问题
class BasicTask():
    def __init__(self):
        self.conn = pymongo.MongoClient("127.0.0.1",27017)
        pass

    def get_response(self,url, headers={}):
        response_json = None

        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            response_json = response.read()
            print response_json
            result = json.loads(response_json)
            return result
        except Exception as ex:
            print response_json
