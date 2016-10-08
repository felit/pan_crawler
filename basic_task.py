# coding: utf8
import urllib2
import json
# 抓取过快问题
class BasicTask():
    def __init__(self):
        pass

    def get_response(url, headers={}):
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            response_json = response.read()
            result = json.loads(response_json)
            return result
        except Exception as ex:
            print response_json
