"""
功能：断点续传，每天触发执行一次
"""
import os
import time
from tools.webservice_client import Webservice_Server
from Config.settings import config
from tools.logging_conf import logger
import json
root_path_backup  = config.get('root_path_backup')

def put_data(buildid):
    """
    buildid: W001
    """
    try:
        filename = root_path_backup + '/' +fr"{buildid}_backup_record.txt"
        if os.path.exists(filename):
            with open(filename, "r") as fileHandler:
                listOfLines = fileHandler.readlines()
                for line in listOfLines:
                    print("%s发送数据..." % line)
                    d = json.loads(line)
                    obj=Webservice_Server(buildingId='440300'+buildid)
                    obj.get_model(data=d)
                    time.sleep(10)
                logger.info("续传完成")
            os.remove(filename)

        else:
            print("无续传数据")

    except Exception as e:

        pass




if __name__ == '__main__':
    obj = put_data(buildid="C125")