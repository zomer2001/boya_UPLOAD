"""
数据订阅软件
@时间2023.3.2
__author:chenquan
# # #XML数据需要先使用Rijndael加密算法加密（KEY和IV由市建设科技促进中心提供）
"""
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
rootPath = os.path.split(BASE_DIR)[0]
sys.path.append(rootPath)

import tools.AES_MODE as AES_MODE
from suds.client import Client
from suds import WebFault
import datetime
import pandas as pd
from Config.settings import config
pd.set_option("expand_frame_repr", False)
root_path_config  = config.get('root_path_config')


class Webservice_Server(object):
    def __init__(self, buildingId):
        try:
            super(Webservice_Server, self).__init__()

            url = "http://energydts.ibronline.cn:46506/DTS.ASMX?WSDL"

            # 尝试创建客户端对象
            try:
                self.client = Client(url)
                print("kk")
            except Exception as e:
                print(f"Error creating Suds client: {e}")
                return

            # 初始化建筑ID
            self.buildingId = buildingId
            self.dateTime = datetime.datetime.now()

            # 尝试加载配置文件
            try:
                self.config_KEY_IV = pd.read_json(root_path_config + '/' + "KEY_IV.json")
                print('Config file loaded successfully')
            except FileNotFoundError:
                print(f"Error: Config file 'KEY_IV.json' not found at {root_path_config}")
            except pd.errors.EmptyDataError:
                print("Error: Config file is empty.")
            except Exception as e:
                print(f"Error loading config file: {e}")

            print('Initialization successful')

        except WebFault as e:
            print(f"SOAP WebFault: {e}")
        except Exception as e:
            print(f"Error during Webservice_Server initialization: {e}")

    def get_model(self,data):
        AES_SECRET_KEY = self.config_KEY_IV[f"{self.buildingId}"].KEY  # 此处16|24|32个字符
        IV = self.config_KEY_IV[f"{self.buildingId}"].IV
        print('key,v')
        message = AES_MODE.AES_ENCRYPT(AES_SECRET_KEY,IV).encrypt(data)
        print('加密成功')
        res = self.client.service.transportEnergyData(self.buildingId, self.dateTime, message)
        # 打印接口返回结果
        print(res)
        return data,res

#
if __name__ == '__main__':

    buildingId = '440300W001'

    data = """<?xml version="1.0" encoding="utf-8"?>
    <root>
      <common>
        <building_id>440300W001</building_id>
        <gateway_id>01</gateway_id>
        <type>report</type>
      </common>
      <data operation="report">
        <sequence>1</sequence>
        <parser>yes</parser>
        <time>20221226160000</time>
        <total>1</total>
        <current>0</current>
        <meter id="T101001" name="T101001" conn="conn">
          <function id="1" name="T101001-1090" coding="" error="0" sample_time="20221226160000">87</function>
        </meter>
      </data>
    </root>
    """

    # # 数据上传发送层
    # obj=Webservice_Server(buildingId)
    # obj.get_model(data)










