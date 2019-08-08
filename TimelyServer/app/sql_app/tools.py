'''
    工具模块 定义了 一些装饰器
'''
from app.sql_app.config_sql import Config_Mysql
import datetime
from dateutil.relativedelta import relativedelta
from functools import wraps
import logging
from mysql import connector as mysql_connector
import pandas as pd


def decorator_database(hostname=Config_Mysql.hostname, username=Config_Mysql.username, password=Config_Mysql.password, database=Config_Mysql.database):
    '''数据库装饰器  连接与关闭数据库 以及异常处理'''
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                conn = mysql_connector.connect(
                    user = username,
                    password=password,
                    host=hostname,
                    database=database
                )
            except Exception as e:
                logging.warning(e)
                return
            kwargs['conn'] = conn
            try:
                res = func(kwargs)
            except Exception as e:
                res = pd.DataFrame()
                logging.warning(e)
            conn.close()
            return res
        return inner
    return outer


def tryExcept(func):
    '''捕获异常'''
    @wraps(func)
    def inner(conn,sql):
        try:
            res = func(conn,sql)
        except Exception as e:
            print(e)
            res = None
            logging.warning(e)
        return res
    return inner


def extend_into_next_month() -> tuple:
    '''
        返回 本月的第几天,当前的年_月,上一个年_月 
    '''
    now = datetime.datetime.now()
    cur_month_day = datetime.date.today().day  # 当月的第几天
    cur_month = now.strftime('%Y_%m')
    last_month = (now + relativedelta(months=-1)).strftime('%Y_%m')
    return now, cur_month_day, cur_month, last_month


def query_byperiod_nogroupby(field, table, date):
    '''格式化根据时间段查询sql'''
    return (Config_Mysql.sql_period_values[0] % (table, field, date, field, date),
                                Config_Mysql.sql_period_values[1] % (table, field, date, field, date),
                                Config_Mysql.sql_period_values[2] % (table, field, date, field, date),
                                Config_Mysql.sql_period_values[3] % (table, field, date, field, date),
                                Config_Mysql.sql_period_values[4] % (table, field, date, field, date, field, date, field, date),)