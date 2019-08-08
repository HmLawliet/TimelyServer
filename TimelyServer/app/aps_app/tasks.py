'''
    定时执行的方法与配置
    execute.py 调用timely_tasks的元组
'''
from app.sql_app.readsql import QueryData
from app.charts_app.charts import Generate_Report
from app.send_app.robot import send_work_notice_file
from app.sql_app.config_sql import Config_Mysql
import datetime
import os


__slots__ = ('timely_tasks',)


# 定时任务方法
def genreta_report_to_send():
    ''' 查询数据,生成报表,发送报表至钉钉工作通知 '''
    p1 = QueryData.query_byperiod()
    date = datetime.datetime.now().date()
    day  = date.weekday()
    day = day if day != 0 else 7
    d1 = QueryData.query_byday(day)

    title = '沃朴日报'
    tmp_list = [ '%s:%s\n' % (key,value)  for key,value in zip(Config_Mysql.sql_period_key1,Config_Mysql.sql_period_key2)]
    notes = '''备注：\n
    时间段分隔说明\n
            %s\n
    多天数据统计说明\n
            统计本周今天之前的数据，每周一统计上周数据
    '''  %  ''.join(tmp_list)
    gr = Generate_Report(title,notes)
    rn = gr.report_name
    tips = '日期 : %s\n 说明: 一天不同时间段的统计数\n' % (datetime.date.today() - datetime.timedelta(1)).strftime('%Y-%m-%d')
    gr.Template_1(p1,tips,draw_line=False)
    tips = '日期 : %s ~ %s\n 说明: 多天的统计数据' % (d1[2][0],d1[2][-1])
    gr.Template_1(d1,tips,isdraw=True)

    file = '%s/report/%s' % (os.path.dirname(os.getcwd()),rn)
    send_work_notice_file(file)


# 定时任务配置
timely_tasks=(
    {
        'func':genreta_report_to_send,
        'trigger':'cron',
        'args':None,
        'kwargs':None,
        'id':'id_grs',
        'name':'name_grs',
        'trigger_args':{
            'day': '*',
            'hour': 8,
            'minute': 0,
            'second': 0,
        }
    },
    # # 模板 
    # def temple():
    #   print(1)
    # {
    #     'func':temple,  # 可调用的方法
    #     'trigger':'cron',  # 触发器  cron 具体详情见 README.MD
    #     'args':None,  # 函数参数
    #     'kwargs':None,  # 函数关键字参数
    #     'id':'id_temple',  # 调度任务job_id
    #     'name':'name_temple',  # 调度任务job_name
    #     'trigger_args':{       # 具体触发器的详细设置
    #         'day': '*',
    #         'hour': '*',
    #         'minute': '*',
    #         'second': '*/10',
    #     }
    # },
)



if __name__ == "__main__":
    pass 
