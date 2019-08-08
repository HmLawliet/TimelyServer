'''
    根据天，时间段来查询 uv,扫描，验伪的统计数据
'''
from app.charts_app.config_charts import Config_Charts
from app.sql_app.config_sql import Config_Mysql, Config_Mysql_FalseCheck
from app.sql_app.config_sql import Config_Mysql_ScanCode, Config_Mysql_UserView
from app.sql_app.tools import tryExcept, decorator_database ,extend_into_next_month,query_byperiod_nogroupby
from collections import OrderedDict
import datetime
from functools import lru_cache
from  mysql.connector.connection_cext import CMySQLConnection
import pandas as pd 
import random


__slots__ = ('QueryData')

@tryExcept
def read_data(sql=None,conn = None):
    '''pandas读取数据'''
    return pd.read_sql(sql,conn)


def concat_bytime(sql,conn,time,df):
    '''dataframe 根据时间来聚合'''
    tmp_df = read_data(sql,conn)
    tmp_df.index=(time,)
    return pd.concat((df,tmp_df)) 


def  get_param(kwargs):
    ''' 解析 kwargs 参数  返回 数据库的连接,天数,dataframe '''
    if 'conn' not in kwargs.keys() or 'day' not in kwargs.keys():
        raise Exception('need two param : conn and day')
    conn = kwargs['conn']
    day = kwargs['day']
    if not isinstance(conn,CMySQLConnection) or not isinstance(day,int):
        raise Exception('conn is connecting Mysql object or param the type of day  is int')
    df = pd.DataFrame()
    return conn,day,df


def query_byday_df(kwargs,cls):
    '''执行不同类型的查询 天 返回值是dataframe'''
    now = datetime.datetime.now()
    conn,day,df = get_param(kwargs)
    for i in range(1, day+1):
        date = (now + datetime.timedelta(days=-i)).strftime('%Y-%m-%d')
        try:
            df = concat_bytime(cls.sql_oneday.format(i),conn,date,df)
        except Exception:
            continue
    return df


@decorator_database()
def query_userview_byday(kwargs) :
    '''
        查询 userview 数量
        返回 字典  key 是时间，value 是统计数
    '''
    return query_byday_df(kwargs,Config_Mysql_UserView) 


@decorator_database()
def query_scancode_byday(kwargs):
    '''
        查询 扫描 数量
        返回 字典  key 是时间，value 是统计数
    '''
    return query_byday_df(kwargs,Config_Mysql_ScanCode)

@decorator_database()
def query_falsecheck_byday(kwargs):
    '''
        查询 验伪 数量
        返回 字典  key 是时间，value 是统计数
    '''
    return query_byday_df(kwargs,Config_Mysql_FalseCheck)



# ====================== 时间段内的统计 ====================
def query_byperiod_df(kwargs,cls):
    '''执行不同类型的查询 时间段 返回值是dataframe'''
    now = datetime.datetime.now()
    conn,day,df = get_param(kwargs)
    for i in range(1, day+1):
        date = (now + datetime.timedelta(days=-i)).strftime('%Y-%m-%d')
        sqls = query_byperiod_nogroupby(cls.field_name_byperiod,cls.table_name_byperiod,date) 
        for index,sql in enumerate(sqls):
            try:
                df = concat_bytime(sql.format(i),conn,'%s_%s' % (index,Config_Mysql.sql_period_key1[index]),df)
            except Exception as e:
                continue
    df = df.groupby(df.index).sum()
    return df 


@decorator_database()
def query_userview_byperiod(kwargs): 
    '''查询访问 时间段'''
    return query_byperiod_df(kwargs,Config_Mysql_UserView)

    

@decorator_database()
def query_scancode_byperiod(kwargs):    
    '''查询扫描 时间段'''
    return query_byperiod_df(kwargs,Config_Mysql_ScanCode)

@decorator_database()
def query_falsecheck_byperiod(kwargs):    
    '''查询验伪 时间段'''
    return query_byperiod_df(kwargs,Config_Mysql_FalseCheck)


def  analysis_data(df,transposition):
    '''将dataframe格式数据转换成python格式'''
    if df.empty:
        return (),()
    if transposition:
        return tuple(df.index)[::-1],tuple([item[0] for item in df.values[::-1]])
    return tuple(df.index),tuple([item[0] for item in df.values])

def format_values(time_iter,value_iter):
    '''对数据格式进行按天整合,目前该方法未使用'''
    od = OrderedDict()
    for index,_ in enumerate(time_iter):
        if index not in od.keys():
            od[index] = []
        for item in value_iter:
            od[index].append(item[index])
    value_res = tuple(od.values())
    return value_res

def comparing(time_list,value_list):
    '''整理数据成报表所需格式'''
    time_len = 0
    time_index = 0
    for index,item in enumerate(time_list):
        tmp_len = len(item)
        if tmp_len > time_len:
            time_len = tmp_len
            time_index = index 
    if time_index == 0:
        return time_list[time_index],value_list
        # time_res = time_list[time_index]
        # return time_res,format_values(time_res,value_list)

    od = OrderedDict({item:0 for item in time_list[time_index]})
    time_res = tuple(od.keys())
    value_res = []
    for key,value in  zip(time_list,value_list):
        od = OrderedDict.fromkeys(od,0)
        for k,v in zip(key,value):
            od[k] = v
        value_res.append(tuple(od.values()))        
    return time_res,value_res
    # return time_res,format_values(time_res,value_res)
    
def binding_color(ax_data,b_data):
    '''将数据绑定颜色'''
    leg_items = [
        (Config_Charts.chose_colors[random.randint(
            0, len(Config_Charts.chose_colors))], Config_Charts.showname[1]),
        (Config_Charts.chose_colors[random.randint(
            0, len(Config_Charts.chose_colors))], Config_Charts.showname[2]),
        (Config_Charts.chose_colors[random.randint(0, len(Config_Charts.chose_colors))], Config_Charts.showname[3])]
    t_data = [tuple([Config_Charts.showname[0]]+list(ax_data)),
              tuple([Config_Charts.showname[1]]+list(b_data[0])),
              tuple([Config_Charts.showname[2]]+list(b_data[1])),
              tuple([Config_Charts.showname[3]]+list(b_data[2])),]
    return t_data,leg_items
       

def format_data(df_tuple,transposition):
    '''格式化数据'''
    time_list,value_list = [],[]
    for df in df_tuple:
        times,values =analysis_data(df,transposition)
        time_list.append(times)
        value_list.append(values)
    ax_data, b_data = comparing(time_list,value_list)
    if not transposition:
        ax_data = Config_Mysql.sql_period_key1
    t_data,leg_items = binding_color(ax_data, b_data)
    return t_data, b_data, ax_data, leg_items


class QueryData:
    '''对外查询数据的接口类'''
    @staticmethod
    @lru_cache()
    def query_byday(day=1,transposition=True):
        '''根据天来查询 uv,sc,fc'''
        uv = query_userview_byday(day=day) 
        sc = query_scancode_byday(day=day)
        fc = query_falsecheck_byday(day=day)
        return format_data((uv,sc,fc,),transposition)

    @staticmethod
    @lru_cache()
    def query_byperiod(day=1,transposition=False):
        '''根据时间段查询 uv,sc,fc'''
        uv = query_userview_byperiod(day=day)
        sc = query_scancode_byperiod(day=day)
        fc = query_falsecheck_byperiod(day=day)
        return format_data((uv,sc,fc,),transposition)


if __name__ == "__main__":
    # df = query_userview_byday(day=3)
    # df = query_scancode_byday(day=1)
    # df = query_falsecheck_byday(day=5)
    # df = query_userview_byperiod(day=1)
    # df = query_scancode_byperiod(day=3)
    # df = query_falsecheck_byperiod(day=2)

    # df = query_byday(day=2)
    df =  query_byperiod(day=1)
    print(df)