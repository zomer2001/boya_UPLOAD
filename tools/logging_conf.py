import os
from loguru import logger
import datetime

from Config.settings import config

root_path_record = config.get('root_path_record')

#指定日志文件存储文件夹
log_dir = os.path.expanduser(root_path_record)

time0 = datetime.datetime.now()

#指定日志文件格式
log_file = os.path.join(log_dir, f"file_{time0.year}-{time0.month}-{time0.day}.log")

#设置rotation参数，以固定文件大小100KB存储文件
logger.add(log_file, rotation = "100KB",retention=1)

#追加compression参数，压缩文件
#logger.add(log_file, rotation = "100KB",compression="zip")


