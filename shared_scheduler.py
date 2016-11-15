# coding:utf8
from basic_task import BasicTask
import time
from shared import Shared
class SharedScheduler(BasicTask):
    def __init__(self):
        BasicTask.__init__(self)
    def run(self):
        uk = self.next_uk()
        while(uk is not None):
            shared = Shared()
            shared.execute()
            uk = self.next_uk()

    def next_uk(self):
        sql = """
            SELECT follow_uk
            FROM accounts
            WHERE is_files_crawler=false AND pubshare_count > 10 limit 1
        """
        cursor = self.mysql_conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result)>0:
            return result[0][0]
        else:
            return None
if __name__=='__main__':
    SharedScheduler().run()
