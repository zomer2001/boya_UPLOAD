from configparser import ConfigParser
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 读取配置文件
cfg = ConfigParser()

cfg.read(os.path.join(BASE_DIR,'config.ini'))

# cfg.read("/Device_Control_Algorithms/tools/config.ini")
config = dict(cfg.items("local_config"))

config0 = dict(cfg.items("database"))

# 本地数据库
db_param = {
    "LOCAL": {
        'host': 'localhost',
        'port': 1433,
        'dbname': 'dlsoftdb',
        'user': 'sa',
        'password': 'Jky@375482356',
        'DBType': 'SQLServer',
        'remark': '本地数据库',
    },
    "SOURCE": {
         'host': 'localhost',
        'port':3306,
        'dbname': 'LFXX_IOServerStatisDB',
        'user': 'root',
        'password': 'Jky@1234',
        'DBType': 'Mysql',
        'remark': '目标数据库',
    }
}

#XML file
xml_param = {
    "XML": {
        'Split_Number': 2,
        'Start': 1,
        'factor': 0.1,
        'remark': 'XML包设置',
    },
}
