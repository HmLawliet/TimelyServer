'''
    项目运行模块 
    python run.py
'''
from log import Log
from app.aps_app.execute import  Scheduler 

# 初始化日志
Log.init_log()

# 执行任务调度
s = Scheduler()
s.start()
