import os
import pymysql
import pymssql
from Config.settings import db_param

#获取数据库连接
def get_conn_db(sys_code='SOURCE'):
    """
    数据库连接获取，此处给出我常用的三种数据库连接
    """
    params = db_param[sys_code]
    host = params['host']
    port = params['port']
    database = params['dbname']
    user = params['user']
    password = params['password']
    db_type = params['DBType'].upper()

    if db_type == "Mysql".upper():
        return pymysql.connect(database=database, user=user, password=password, host=host, port=port)
    # elif db_type == "Oracle".upper():
    #     os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    #     dsn = cx_Oracle.makedsn(host, port, service_name=database)
    #     conn = cx_Oracle.connect(user, password, dsn=dsn)
    #     return conn
    elif db_type == 'SQLServer'.upper():
        return pymssql.connect(host=host, user=user, password=password, database=database, charset="utf8")
    else:
        raise Exception("%s数据库连接失败. " % sys_code)