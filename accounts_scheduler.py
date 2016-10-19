# coding:utf8
# 按follow抓取
# 按fans抓取
from basic_task import BasicTask
from accounts import Accounts


class AccountsScheduler(BasicTask):
    def __init__(self):
        BasicTask.__init__(self)

    def inter(self):
        account = 2
        while (account is not None):
            account = self.db.accounts.find_one({'crawler': {'$exists': True}, 'follow_count': {'$gt': 10}})
            if account is not None:
                Accounts(account['follow_uk']).execute()


if __name__ == '__main__':
    scheduler = AccountsScheduler()
    scheduler.inter()