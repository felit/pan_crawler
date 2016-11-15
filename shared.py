# coding: utf8
from basic_task import BasicTask
from time import sleep
import time
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
        sql = """
            update accounts set is_files_crawler=True where follow_uk='%s'
        """ %(self.uk)
        print sql
        cursor = self.mysql_conn.cursor()
        cursor.execute(sql)
        self.mysql_conn.commit()

    def get_first_shared_files(self):
        url =self.shared_url_tpl.format(start=0, uk=self.uk, limit=self.limit)
        response_json = self.get_response(url, self.params)
        print(response_json)
        self.total_count = response_json['total_count']
        self.save_records(response_json['records'])

    def crawler_shared_files(self):
        if self.total_count > self.limit:
            for i in range(1, self.total_count / self.limit):
                url = self.shared_url_tpl.format(start=i * self.limit, uk=self.uk, limit=self.limit)
                records = self.get_url(url)
                # print records
                self.save_records(records)

    def get_url(self,url):
        response_json = self.get_response(url, self.params)
        while(not response_json.has_key('records')):
            response_json = self.get_response(url, self.params)
            if(not response_json.has_key('records')):
                sleep(self.sleep_time_len)
                print url
            else:
                pass
        return response_json['records']

    def save_records(self,records):
        # TODO存储至mysql
        insert_sql = """
            INSERT INTO yunpan.shared_files(shorturl,like_count, dCnt, category, title, comment_count,
                    feed_time,public, username, source_uid, like_status, feed_type, vCnt, filecount, description,
                    third, data_id, tCnt, clienttype, isdir, server_filename, path, size, avatar_url, shareid, uk, source_id)
             values('{0[shorturl]}',{0[like_count]},{0[dCnt]},{0[category]},'{0[title]}',{0[comment_count]},'{0[feed_time]}',{0[public]},
             '{0[username]}','{0[source_uid]}',{0[like_status]},'{0[feed_type]}','{0[vCnt]}',{0[filecount]},'{0[description]}',{0[third]},
             '{0[data_id]}',{0[tCnt]},{0[clienttype]},{0[isdir]},'{0[server_filename]}','{0[path]}',{0[size]},'{0[avatar_url]}','{0[shareid]}','{0[uk]}','{0[source_id]}')
        """
        for record in records:
            if record.has_key('feed_time'):
                record['feed_time']=time.strftime('%Y-%m-%d %H-%M-%S',time.gmtime(record['feed_time']/1000))

            if not record.has_key('shorturl'):
                record['shorturl']=''
            if not record.has_key('description'):
                record['description']=''

            if not record.has_key('size'):
                record['size']='Null'
            if record.has_key('filelist'):
                for file in record['filelist']:
                    if file.has_key('isdir'):
                        if file['isdir']==1:
                            record['isdir'] = True
                            print file['path']
                        else:
                            record['isdir'] = False
                            record['size'] = file['size']
                    else:
                        print record
                    if file.has_key('path'):
                        record['path']=file['path']
                    else:
                        record['path'] = ''
                    if not file.has_key('server_filename'):
                        record['server_filename']=''
                    else:
                        print file['server_filename']
                        record['server_filename']=file['server_filename']

                    if not record.has_key('isdir'):
                        record['isdir']='Null'
                        print record
                    if not record.has_key('path'):
                        record['path']=''
                    print insert_sql.format(record)
                    self.cursor.execute(insert_sql.format(record))
        # self.cursor.close()
        self.mysql_conn.commit()

if __name__ == '__main__':
    shared = Shared('2636470911')
    # {u'dir_cnt': 1, u'shorturl': u'1bn2FUDh', u'like_count': 0, u'dCnt': 1, u'category': 6, u'title': u'PDF\u9605\u8bfb\u5668', u'comment_count': 0, u'feed_time': 1415039932000, u'public': u'1', u'username': u'51**jx', u'source_uid': u'931830473', u'like_status': 0, u'feed_type': u'share', u'vCnt': 27, u'filecount': 1, u'desc': u'', u'third': 0, u'data_id': u'8777071490347001723', u'tCnt': 1, u'clienttype': 0, u'filelist': [{u'category': 6, u'isdir': 1, u'server_filename': u'PDF\u9605\u8bfb\u5668', u'sign': u'6f285c34e643a1430db6e787857817f91224391c', u'fs_id': 1679724544, u'time_stamp': 1478927224, u'path': u'%2F%E5%BA%94%E7%94%A8%E8%BD%AF%E4%BB%B6%2FPDF%E9%98%85%E8%AF%BB%E5%99%A8', u'md5': u'0', u'size': 1024}], u'avatar_url': u'https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/item/c99a8a37.jpg', u'shareid': u'2000682979', u'uk': 2587068245, u'source_id': u'2000682979'}
    shared = Shared('2587068245') #有文件夹
    # {u'dir_cnt': 1, u'shorturl': u'1hs2nnFY', u'like_count': 0, u'dCnt': 0, u'category': 6, u'title': u'\u540d\u5e08\u5e26\u4f60\u6765\u5237\u9898 8\u67084\u5185\u6709\u66f4\u65b0', u'comment_count': 0, u'feed_time': 1472117662069, u'public': u'1', u'username': u'\u533b*\u7cbe\u9009', u'source_uid': u'1199254137', u'like_status': 0, u'feed_type': u'share', u'vCnt': 26, u'filecount': 1, u'desc': u'', u'third': 0, u'data_id': u'7919125319332336499', u'tCnt': 17, u'clienttype': 0, u'filelist': [{u'category': 6, u'isdir': 1, u'server_filename': u'\u540d\u5e08\u5e26\u4f60\u6765\u5237\u9898 8\u67084\u5185\u6709\u66f4\u65b0', u'sign': u'7d2083dfdb678410b4aa07eb70ad92a7c681e85f', u'fs_id': 5547769292528, u'time_stamp': 1478927332, u'path': u'%2F2016%E8%80%83%E7%A0%94%E5%85%A8%E7%A8%8B%E4%B8%8D%E5%8A%A0%E5%AF%86%2F2016%E5%B9%B4%E6%94%BF%E6%B2%BB%2F2016%E5%B9%B4xdf%20%E8%80%83%E7%A0%94%E6%94%BF%E6%B2%BB%2F2016%E5%B9%B4%E6%96%B0%E4%B8%9C%E6%96%B9%E6%94%BF%E6%B2%BB%E5%BC%BA%E5%8C%96%E7%8F%AD%2F%E5%90%8D%E5%B8%88%E5%B8%A6%E4%BD%A0%E6%9D%A5%E5%88%B7%E9%A2%98%208%E6%9C%884%E5%86%85%E6%9C%89%E6%9B%B4%E6%96%B0', u'md5': u'0', u'size': 1024}], u'avatar_url': u'https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/item/792a7b47.jpg', u'shareid': u'2437997843', u'uk': 709048228, u'source_id': u'2437997843'}
    shared = Shared('709048228') #有文件夹列表
    shared.execute()