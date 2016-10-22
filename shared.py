# coding: utf8
from basic_task import BasicTask


class Shared(BasicTask):
    """
    返回分享内容
    """

    def __init__(self, follow_uk='2636470911'):
        BasicTask.__init__(self)
        self.uk = follow_uk
        self.limit = 20
        self.shared_url_tpl = "https://yun.baidu.com/pcloud/feed/getsharelist?auth_type=1&start={start}&limit={limit}&query_uk={uk}"
        self.shared_list_url_tpl = "https://yun.baidu.com/share/list?uk={uk}&shareid={shareid}&page=1&num=100&dir={dir}&order=time&desc=1"
        self.params = {'Referer': 'https://yun.baidu.com',
                       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
                       'X-Requested-With': 'XMLHttpRequest'
        }

    def get_shared(self):

        # 分享
        response_json = self.get_response(
            'https://yun.baidu.com/pcloud/feed/getsharelist?auth_type=1&start=0&limit=20&query_uk=1260121397',
            self.params)
        for record in response_json['records']:
            print record['shorturl'], record['title']

        share_list = "https://yun.baidu.com/share/list?uk=1260121397&shareid=1846820413&page=1&num=100&dir=%2F%E6%88%91%E7%9A%84%E9%9F%B3%E4%B9%90%2FM_backup%2FBD003%2F%E5%93%88%E5%A1%9E%E3%80%81%E8%83%A1%E6%A2%85%E5%B0%94%E3%80%81%E9%9C%8D%E5%A4%AB%E6%9B%BC%E6%9B%BC%E9%99%80%E9%93%83%E5%8D%8F%E5%A5%8F%E6%9B%B2&order=time&desc=1"
        response_json = self.get_response(share_list, self.params)
        for row in response_json['list']:
            print "%s\t%s\t%s\t%s\t%s" % (
                row['isdir'], row['category'], row['size'], row['server_filename'], row['path'])
            # print row

    def execute(self):
        self.get_first_shared_files()
        self.crawler_shared_files()
        self.db.accounts.update({'follow_uk': self.uk}, {'$set': {'crawler_files': True}}, upsert=True)

    def get_first_shared_files(self):
        url =self.shared_url_tpl.format(start=0, uk=self.uk, limit=self.limit)
        # print self.params
        response_json = self.get_response(url, self.params)
        # print(response_json)
        self.total_count = response_json['total_count']
        self.db.shared_files.insert_many(response_json['records'])

    def crawler_shared_files(self):
        if self.total_count > self.limit:
            for i in range(1, self.total_count / self.limit):
                url = self.shared_url_tpl.format(start=i * self.limit, uk=self.uk, limit=self.limit)
                response_json = self.get_response(url, self.params)
                # update by shorturl
                self.db.shared_files.insert_many(response_json['records'])


if __name__ == '__main__':
    shared = Shared('2636470911')
    shared.execute()