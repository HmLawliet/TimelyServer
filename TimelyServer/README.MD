项目说明：
    该项目是定时执行任务的项目
    设置定时任务，执行sql查询，生成pdf报表，并将pdf报表发送至钉钉工作通知
    
    该项目记录自己的成长
    如果能对各位有所帮助,也十分开心。
    开源带来快乐
    对robot与mysql里一些公司隐秘信息都用其他信息代替了

1 安装
    pip install apscheduler
    pip install mysql-connector-python
    pip install reportlab
    pip install requests
    pip install pandas

备注：使用的环境是 centos7  anaconda3  python3.7

2 结构
    aps_app   任务调度
        execute.py  调度类  因项目场景 用的BlockingScheduler
        tasks.py   配置执行的任务  ----> 用户可以在此文件中按模块中格式添加任务
    charts_app  生成图表
        charts.py  图表，直方图，折线图 并生成pdf 文件
        config_charts.py    生成charts的一些配置文件
    send_app  发送pdf至钉钉工作通知
        config_send.py   发送的文件的链接   实现 阿里钉钉的提供的接口
        robot.py  首先要在钉钉管理后台创建小程序 获取 agent_id,appkey,appsecret ,因时间问题目前仅仅实现通过钉钉通知发送文件
    sql_app  执行查询数据任务
        config_sql.py   配置查询sql的一些信息  
        readsql.py    执行查询sql的函数
        tools.py    执行查询所需要的工具函数
    log.py   简单初始化记录日志
    README.MD   对项目的简单说明
    run.py   您可通过run.py直接运行该定时任务
    SimSun.ttf  是报表生成所以依赖的字体文件， 您可以从网上下载喜欢的字体来替代
    
备注：之所以将每个app的配置文件都分开，为了考虑以后会增加或者删除功能，能保证之前的功能尽可能少受影响

3 相关信息记录

apscheduler 库的简述

apscheduler api 的官网地址：
    https://apscheduler.readthedocs.io/en/latest/

配置参数
    实例化调度器（配置参数）
    实例 add_job(具体方法)
    调用 start()方法

选择调度器
    BlockingScheduler: use when the scheduler is the only thing running in your process

    BackgroundScheduler: use when you’re not using any of the frameworks below, and want the scheduler to run in the background inside your application

    AsyncIOScheduler: use if your application uses the asyncio module

    GeventScheduler: use if your application uses gevent

    TornadoScheduler: use if you’re building a Tornado application

    TwistedScheduler: use if you’re building a Twisted application

    QtScheduler: use if you’re building a Qt application

选择触发器
    date: use when you want to run the job just once at a certain point of time

    interval: use when you want to run the job at fixed intervals of time

    cron: use when you want to run the job periodically at certain time(s) of day
        cron：定时任务，即在每个时间段执行任务。
        参数如下：

        second (int|str) – 秒 (0-59)
        minute (int|str) – 分钟 (0-59)
        hour (int|str) – 小时 (0-23)
        day_of_week (int|str) – 一周中的第几天 (0-6 or mon,tue,wed,thu,fri,sat,sun)
        day (int|str) – 日 (1-31)
        week (int|str) – 一年中的第几周 (1-53)
        month (int|str) – 月 (1-12)
        year (int|str) – 年(四位数)
        start_date (datetime|str) – 最早开始时间
        end_date (datetime|str) – 最晚结束时间
        timezone (datetime.tzinfo|str) – 时区

    calendarinterval: use when you want to run the job on calendar-based intervals, at a specific time of day

选择执行器
    AsyncIOExecutor  ---> AsyncIOScheduler
    DebugExecutor
    PoolExecutor   ---> BackgroundScheduler/BlockingScheduler/TornadoScheduler
        ThreadPoolExecutor(max_workers=10)
        ProcessPoolExecutor(max_workers=10)
    GeventExecutor  ---> GeventScheduler
    TwistedExecutor  ---> TwistedScheduler


基类 BaseScheduler()
    add_job(func, trigger=None, args=None, kwargs=None, id=None, name=None, misfire_grace_time=undefined, coalesce=undefined, max_instances=undefined, next_run_time=undefined, jobstore='default', executor='default', replace_existing=False, **trigger_args)
    start(paused=False)   raise  SchedulerAlreadyRunningError RuntimeError


参数说明
    add_job 参数 replace_existing=True 防止作业的重复添加
    add_job 参数 misfire_grace_time=30 定时任务的过期数
    add_job 参数 coalesce=True  积攒多次的任务只执行一次


钉钉开发
    dingtalk-sdk 的官方文档：
        https://dingtalk-sdk.readthedocs.io/zh_CN/latest/
    钉钉开发文档的官方地址：
        https://open-doc.dingtalk.com/microapp/serverapi3/rg1occ













