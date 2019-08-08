import logging
import datetime
import os

__slots__ = ['Log']


class Log:
    '''
    日志
    '''
    @staticmethod
    def init_log():
        log_path = os.path.dirname(os.getcwd())+ '/logfile/'
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        log_name = log_path + 'apscheduler.log'

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=log_name,
            filemode='a')




if __name__ == "__main__":
    pass
