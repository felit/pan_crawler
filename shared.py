# coding: utf8
from basic_task import BasicTask


class Shared(BasicTask):
    """
    返回分享内容
    """

    def __init__(self):
        BasicTask.__init__(self)

    def get_shared(self):
        params = {'Referer': 'https://yun.baidu.com',
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
                  'X-Requested-With': 'XMLHttpRequest'
        }
        # 分享
        response_json = self.get_result(
            'https://yun.baidu.com/pcloud/feed/getsharelist?auth_type=1&start=0&limit=20&query_uk=1260121397', params)
        for record in response_json['records']:
            print record['shorturl'], record['title']

        share_list = "https://yun.baidu.com/share/list?uk=1260121397&shareid=1846820413&page=1&num=100&dir=%2F%E6%88%91%E7%9A%84%E9%9F%B3%E4%B9%90%2FM_backup%2FBD003%2F%E5%93%88%E5%A1%9E%E3%80%81%E8%83%A1%E6%A2%85%E5%B0%94%E3%80%81%E9%9C%8D%E5%A4%AB%E6%9B%BC%E6%9B%BC%E9%99%80%E9%93%83%E5%8D%8F%E5%A5%8F%E6%9B%B2&order=time&desc=1"
        response_json = self.get_result(share_list, params)
        for row in response_json['list']:
            print "%s\t%s\t%s\t%s\t%s" % (
                row['isdir'], row['category'], row['size'], row['server_filename'], row['path'])
            # print row

