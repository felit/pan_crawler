# coding:utf8
# 按follow抓取
# 按fans抓取　太多，且很多共享内容为空
# 进程死掉的时候，重启进程
from basic_task import BasicTask
from accounts import Accounts
import time

class AccountsScheduler(BasicTask):
    def __init__(self):
        BasicTask.__init__(self)

    def inter(self):
        sql = """
            SELECT follow_uk,is_follow_crawler
            FROM yunpan.accounts
            WHERE is_follow_crawler is FALSE AND follow_count>0
            LIMIT 1
        """
        time.sleep(0.5)
        cursor = self.mysql_conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if result is not None and len(result) > 0:
            account = result[0][0]
        else:
            account = None
        while (account is not None):
            account = Accounts(account).execute()


if __name__ == '__main__':
    scheduler = AccountsScheduler()
    scheduler.inter()