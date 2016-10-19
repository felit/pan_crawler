# coding: utf8
import urllib2
import json
# 抓取过快问题

URL_SHARE = 'http://yun.baidu.com/pcloud/feed/getsharelist?auth_type=1&start={start}&limit=20&query_uk={uk}&urlid={id}'

url = "https://yun.baidu.com/pcloud/friend/getfollowlist?query_uk=1883386731&limit=24&start={start}&channel=chunlei&clienttype=0&web=1"
"""
{
 u'fans_count': 468,
 u'avatar_url': u'https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/item/a738b109.jpg',
 u'pubshare_count': 125,
 u'follow_uname': u'\u6e05**ue',
 u'follow_count': 390,
 u'user_type': 0,
 u'intro': u'',
 u'album_count': 0,
 u'is_vip': 0,
 u'follow_uk': 940435822,
 u'type': -1,
 u'follow_time': 1401010410
}
"""


def get_response(url, headers={}):
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        response_json = response.read()
        result = json.loads(response_json)
        return result
    except Exception as ex:
        print response_json


def get_follows(result):
    for row in result['follow_list']:
        # print "{follow_uname}\t{pubshare_count}\t{follow_count}".format(row)
        print "%s\t%s\t%s\t%s\t%s" % (row['follow_uname'],
                                      row['follow_uk'],
                                      row['fans_count'],
                                      row['pubshare_count'],
                                      row['follow_count'])


# result = get_result(url.format(start=0))
# print result
# get_follows(result)
# # 粉丝总数年
# total_num = result['total_count']
# for i in range(1, total_num / 25):
#     result = get_result(url.format(start=i * 25))
#     get_follows(result)



#
params = {'Referer': 'https://yun.baidu.com',
          'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
          'X-Requested-With': 'XMLHttpRequest'
}
# 分享
# response_json = get_result('https://yun.baidu.com/pcloud/feed/getsharelist?auth_type=1&start=0&limit=20&query_uk=1260121397', params)
response_json = get_response('https://yun.baidu.com/pcloud/feed/getsharelist?auth_type=1&start=0&limit=20&query_uk=2636470911', params)
for record in response_json['records']:
    print record
    # print record['shorturl'], record['title']
#
# share_list = "https://yun.baidu.com/share/list?uk=1260121397&shareid=1846820413&page=1&num=100&dir=%2F%E6%88%91%E7%9A%84%E9%9F%B3%E4%B9%90%2FM_backup%2FBD003%2F%E5%93%88%E5%A1%9E%E3%80%81%E8%83%A1%E6%A2%85%E5%B0%94%E3%80%81%E9%9C%8D%E5%A4%AB%E6%9B%BC%E6%9B%BC%E9%99%80%E9%93%83%E5%8D%8F%E5%A5%8F%E6%9B%B2&order=time&desc=1"
# response_json = get_result(share_list, params)
# for row in response_json['list']:
#     print "%s\t%s\t%s\t%s\t%s" % (row['isdir'], row['category'], row['size'], row['server_filename'], row['path'])
#     # print row
