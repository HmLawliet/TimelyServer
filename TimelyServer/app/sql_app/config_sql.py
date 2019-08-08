
class Config_Mysql:
     hostname = '123.123.123.123'
     username = 'test'
     password = 'test'
     database = 'antifake'
     sql_period_key1 = ('morning', 'forenoon', 'noon', 'afternoon', 'evening',)
     sql_period_key2 =('06:30:00~08:00:00','08:00:00~11:30:00','11:30:00~14:00:00','14:00:00~17:30:00','00:00:00~06:30:00 - 17:30:00~23:59:59')
     sql_period_values = (
          'select count(1) as count from %s where %s >= "%s 06:30:00" and %s <= "%s 08:00:00" ;',
          'select count(1) as count from %s where %s >= "%s 08:00:00" and %s <= "%s 11:30:00" ;',
          'select count(1) as count from %s where %s >= "%s 11:30:00" and %s <= "%s 14:00:00" ;',
          'select count(1) as count from %s where %s >= "%s 14:00:00" and %s <= "%s 17:30:00" ;',
          'select count(1) as count from %s where (%s >= "%s 00:00:00" and %s <= "%s 06:30:00") or (%s >= "%s 17:30:00" and %s <= "%s 23:59:59");',
          )

class Config_Mysql_UserView(Config_Mysql):
     sql_oneday = 'select count(1) as count from  ac_point_log where point_code = "mn_e120"  and date_format(point_time,"%Y-%m-%d") = date_format(SUBDATE(now(),{}),"%Y-%m-%d");'
     table_name_byperiod = 'ac_point_log'
     field_name_byperiod = 'point_time'

class Config_Mysql_ScanCode(Config_Mysql):
    sql_oneday = 'select count(1) as count from  ac_scan_log where date_format(scan_time,"%Y-%m-%d") = date_format(SUBDATE(now(),{}),"%Y-%m-%d");'
    table_name_byperiod = 'ac_scan_log'
    field_name_byperiod = 'scan_time'


class Config_Mysql_FalseCheck(Config_Mysql):
     sql_oneday = 'select count(1) as count from  ac_antifake_log where date_format(verify_time,"%Y-%m-%d") = date_format(SUBDATE(now(),{}),"%Y-%m-%d");'
     table_name_byperiod = 'ac_antifake_log'
     field_name_byperiod = 'verify_time'


if __name__ == "__main__":
     pass 