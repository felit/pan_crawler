# coding: utf8
from basic_task import BasicTask
# 抓取过快问题通过sleep(1)解决掉
# 抓取判重问题
# 最后检测时间
from time import ctime, sleep
import time
import datetime

class Accounts(BasicTask):
    """
    取当前帐户的关联信息
    """

    def __init__(self, follow_uk='1493351221'):
        BasicTask.__init__(self)
        self.uk = follow_uk
        print(self.uk)
        self.total = 0
        self.limit = 24
        #
        self.url_tpl = "https://yun.baidu.com/pcloud/friend/getfollowlist?query_uk={uk}&limit={limit}&start={start}&channel=chunlei&clienttype=0&web=1"
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

    def execute(self):
        """
        生成所在的任务
        :return:
        """
        self.get_first_task()
        self.gen_task()
        self.update_follow_uk()
        return self.next_follow_uk()
        # 更新 self.uk对的信息

    def update_follow_uk(self):
        sql = """
            update yunpan.accounts
            set is_follow_crawler = TRUE
            where follow_uk='%s'
        """ % self.uk
        print sql
        cursor = self.mysql_conn.cursor()
        cursor.execute(sql)

        cursor.close()
        self.mysql_conn.commit()

    def next_follow_uk(self):
        sql = """
            SELECT follow_uk,is_follow_crawler
            FROM yunpan.accounts
            WHERE is_follow_crawler is FALSE AND follow_count>0
            LIMIT 1
        """
        cursor = self.mysql_conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]
    def save_follows(self, follow_list):
        query_sql = """
            select id from yunpan.accounts where follow_uk='{follow_uk}'
        """
        insert_sql = """
            INSERT INTO yunpan.accounts(follow_uk, fans_count, parent_follow_uk, avatar_url,
            pubshare_count, follow_uname, follow_count, user_type, intro, album_count,
            is_vip, type, follow_time, create_time, update_time, is_follow_crawler, is_files_crawler)
            VALUES('{0[follow_uk]}',{0[fans_count]},'{0[parent_follow_uk]}','{0[avatar_url]}',{0[pubshare_count]},
            '{0[follow_uname]}',{0[follow_count]},{0[user_type]},'{0[intro]}',{0[album_count]},{0[is_vip]},{0[type]},
            '{0[follow_time]}','{0[create_time]}','{0[update_time]}',{0[is_follow_crawler]},{0[is_files_crawler]})
        """
        update_sql = """
            UPDATE yunpan.accounts
            SET fans_count={0[fans_count]} ,
                parent_follow_uk='{0[parent_follow_uk]}',
                avatar_url='{0[avatar_url]}',
                pubshare_count={0[pubshare_count]},
                follow_uname='{0[follow_uname]}',
                follow_count={0[follow_count]},
                user_type={0[user_type]},
                intro='{0[intro]}',
                album_count={0[album_count]},
                is_vip={0[is_vip]},
                type={0[type]},
                follow_time='{0[follow_time]}',
                update_time='{0[update_time]}',
                is_follow_crawler={0[is_follow_crawler]}
            WHERE follow_uk={0[follow_uk]}
        """
        # --- create_time='{create_time}',
        # is_files_crawler={0[is_files_crawler]},

        cursor = self.mysql_conn.cursor()
        for row in follow_list:
            uk = str(row['follow_uk'])
            row['follow_uk'] = uk
            row['parent_follow_uk'] = self.uk
            row['follow_uname']=row['follow_uname'].replace('\'','\\\'')
            row['intro']=row['intro'].replace('\'','\\\'')
            row['follow_time']=time.strftime('%Y-%m-%d %H-%M-%S',time.gmtime(row['follow_time']))
            cursor.execute(query_sql.format(follow_uk=uk))
            result = cursor.fetchall()
            row['update_time'] = datetime.datetime.today()
            if (len(result) > 0):
                row['parent_follow_uk'] = '%s,%s' % (result[0][0], row['parent_follow_uk'])
                row['is_follow_crawler']=True
                sql = update_sql.format(row)
            else:
                row['create_time']=datetime.datetime.today()
                row['is_follow_crawler']=False
                row['is_files_crawler']=False
                print insert_sql.format(row)
                sql = insert_sql.format(row)#update_time
            try:
                cursor.execute(sql)
            except Exception,ex:
                print ex
        cursor.close()
        self.mysql_conn.commit()

    def get_first_task(self):
        url = self.url_tpl.format(uk=self.uk, limit=self.limit, start=0)
        result = self.get_response(url)
        if result is not None and (result.has_key('follow_list')):
            self.total = result['total_count']
            self.save_follows(result['follow_list'])
            sleep(1)
        else:
            print url
            sleep(self.sleep_time_len)


    def gen_task(self):
        """
        生成抓取任务
        :return:
        """
        for i in range(1, self.total / self.limit):
            url = self.url_tpl.format(uk=self.uk, limit=self.limit, start=i * self.limit)
            result = self.get_response(url)
            if (result.has_key('follow_list')):
                self.save_follows(result['follow_list'])
            else:
                sleep(self.sleep_time_len)


if __name__ == '__main__':
    accounts = Accounts()
    accounts.execute()