'''
执行定时任务模块:
    代理监听类
    执行任务类
'''
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED
from apscheduler.executors.pool import ProcessPoolExecutor,ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from app.aps_app.tasks import timely_tasks
import os 
import redis


__slots__ = ('Scheduler')

class ListenerHandler:
    '''apscheduler 执行错误的监听类 需要任务调用时注册监听'''
    @staticmethod
    def listener(event):
        # 将执行错误的或者将任务错过的记录并发送通知
        logging.warning('code---> %s' % event.code)
        logging.warning('exception---> %s' % event.exception)
        logging.warning('job_id---> %s' % event.job_id)
        logging.warning('scheduled_run_time---> %s' % event.scheduled_run_time)
        logging.warning('traceback---> %s' % event.traceback)
        

class Scheduler:
    '''定时任务注册类'''
    def __init__(self,tasks=()):
        if not hasattr(Scheduler,'_scheduler'):
            _scheduler = Scheduler.get_instance()
        self.scheduler = _scheduler
        self.job_ids = {task['id'] for task in tasks}
        self.scheduler.add_listener(ListenerHandler.listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED)

    @staticmethod
    def get_instance():
        '''获得单例实例'''
        jobstores = {
            'default': RedisJobStore(0),
        }
        executors = {
            'default': ThreadPoolExecutor(8),
            'processpool': ProcessPoolExecutor(4)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, daemonic=False)
        return scheduler

    def _flushredis(self):
        '''刷新 存储在redis 的定时任务'''
        red = redis.Redis()
        red.flushdb()

 
    def _add_task(self, tasks):
        '''添加作业'''
        if not isinstance(tasks,list) and not isinstance(tasks,tuple):
            raise Exception('The type of the incoming value must be list or tuple')
        for task in tasks:
            self.scheduler.add_job(func=task['func'], trigger=task['trigger'],args=task['args'], id=task['id'],
                name=task['name'],**task['trigger_args'])
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        try:
            g = self.scheduler.start()
            g.join()
        except (KeyboardInterrupt,SystemExit):
            pass 


    def start(self,tasks=timely_tasks) -> None:
        '''
        启动作业
        '''
        self._flushredis()
        self._add_task(tasks)
        

if __name__ == "__main__":
    s = Scheduler()
    s.start()
