# coding: utf8
from basic_task import BasicTask
# 抓取过快问题
# 抓取判重问题
# 最后检测时间
class Accounts(BasicTask):
    """
    取当前帐户的关联信息
    """

    def __init__(self):
        BasicTask.__init__(self)
        self.uk = '1883386731'
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

    def save_follows(self, follow_list):
        # 保存follow记录
        pass

    def get_first_task(self):
        url = self.url_tpl.format(uk=self.uk, limit=self.limit, start=0)
        result = self.get_response(url)
        self.total = result['total_count']
        self.save_follows(result['get_follows'])


    def gen_task(self):
        """
        生成抓取任务
        :return:
        """
        for i in range(1, self.total / self.limit):
            print i