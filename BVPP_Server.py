from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_user_auth.site import AuthAdminSite
from datetime import datetime
from fastapi_scheduler import SchedulerAdmin
#在fastapi异步框架中，选择AsyncOScheduler调度程序，默认使用sqlite持久化定时任务，不至于重启就失效
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from sqlmodel import SQLModel
from tools.get_data_from_api import  Get_datas
from tools.Put_MQTT import Pub_Server
import time
import json
import struct
import random
import sys
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
rootPath = os.path.split(BASE_DIR)[0]
sys.path.append(rootPath)
from Config.settings import config, config0
from Config.template import template_send,byte_types

root_path_config = config.get('root_path_config')

topic_set = config0.get('topic')

# 创建FastAPI应用
app = FastAPI()
# 创建AdminSite实例
site = AuthAdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///admisadmin.db'))
# site = AuthAdminSite(settings=Settings(database_url_async='mysql+aiomysql://root:root@localhost:3306/amisadmin'))
auth =site.auth

Scheduler = AsyncIOScheduler(jobstore={'default':SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')})

# 创建定时任务调度器`SchedulerAdmin`实例
scheduler = SchedulerAdmin.bind(site)
#定时任务方式：1、date，固定时间执行一次 2、interval，固定间隔时间循环执行3、cron，crontab表达式，最为灵活

with open(root_path_config + '/' + 'Branch_code1.json') as f:
    data = json.load(f)

#寄存器数据
_Meterstate = [[0]*19]

def change_format(parm,arr_):
    """将数据按模板整理成十六进制数组"""
    datain = dict(zip(parm, arr_))
    length = 0
    for i in template_send:
        length += byte_types[template_send[i]['type']]['length']
    arr = []
    type = '>'
    for i in range(len(template_send)):
        type += template_send[i]['type']
        if template_send[i]['name'] in datain:

            # print('template_send',template_send[i]['name'])

            x = int(datain[template_send[i]['name']] * template_send[i]['mtp'])
            if byte_types[template_send[i]['type']]['minvalue'] <= x <= byte_types[template_send[i]['type']]['maxvalue']:
                arr.append(x)
            else:
                arr.append(byte_types[template_send[i]['type']]['default'])
        else:
            arr.append(byte_types[template_send[i]['type']]['default'])

    dataout = struct.pack(type, *arr)
    return dataout

def loadJsonData():
    # 加载json
    with open(r"D:\Data_upload_tool_Kangtai\names1.json", encoding='utf-8') as data:
        # content = data.read()
        # jsonData = json.loads(content).get('data')['meters']
        jsonData = json.load(data)
        # .get('data')['meters']
        print(jsonData)

        dict_ = jsonData.get('meters')
        print('Meters', dict_)

        nested_list=[]

        for i in range(len(dict_)):
            # print(f"第{i}块表", dict_[i])
            dict_s = dict_[i]
            # 固定参数为缺省值
            # key = dict_s.get('meterId')
            # id = data.get(f'{key}')
            if dict_s.get('cabinetId') in [1643188726637314050,1643189909485568003,1643189909485568012,1643189909485568021,1643189909485568029,
                                           1643189909485568038,1643189909485568047,1643189909485568053,1643179275125571586]:
                arrs_ = [1,int(dict_s.get('powerTotalYg')), int(dict_s.get('powerTotalWg')),
                         int(dict_s.get('powerTotalSz')), int(dict_s.get('powerYgA')), \
                         int(dict_s.get('powerYgB')), int(dict_s.get('powerYgC')), int(dict_s.get('powerWgA')),
                         int(dict_s.get('powerWgB')), int(dict_s.get('powerWgC')), \
                         int(dict_s.get('energyZxyg')), int(dict_s.get('voltageA')), int(dict_s.get('voltageB')),
                         int(dict_s.get('voltageC')), int(dict_s.get('currentA')), \
                         int(dict_s.get('currentB')), int(dict_s.get('currentC')), int(dict_s.get('frequencyA')),
                         int(dict_s.get('powerFactorTotal'))]
                # print(arrs_)
                nested_list.append(arrs_)

        #多台变压器数据合并计算
        # 多维数组
        w3 = np.array(nested_list)
        #掩码
        temp = np.ma.masked_array(w3, mask=w3 == 0)
        V = temp.mean(axis=0, dtype=int)
        Value = temp[:, 1].sum(axis=0, dtype=int)
        V[1] = Value
        RES = list(map(int, V.tolist()))

    #
        bytes = change_format(parm=['powerTotalYg', 'powerTotalWg', 'powerTotalSz', 'powerYgA', 'powerYgB', 'powerYgC', 'powerWgA', 'powerWgB',
          'powerWgC', 'energyZxyg', 'voltageA', 'voltageB', 'voltageC', 'currentA', 'currentB', 'currentC',
          'frequencyA', 'powerFactorTotal'],arr_=RES)

        _Meterstate[0]=RES

    return bytes

def get_data_from_api():
    try:
        start = datetime.datetime.now()
        # 转换为int类型的10位时间戳
        timestam = int(time.time())
        time_new = str(timestam)
        params = {"apiKey": '1555312928870420483',
                  "timestamp": time_new}
        res = Get_datas().get_data(params)

        if res:
            dict_ = res.get('meters')
            print('Meters',dict_)

    finally:
        table_name = 'meter'
        # 根据序列号判断是否执行续传检查
        end = datetime.datetime.now()
        s = (end - start).total_seconds()

        print('数据导出: %s, 耗时: %s 秒' % (table_name, s))
        # logger.info('数据导出: %s, 耗时: %s 秒' % (table_name, s))


#定时上传数据到MQTT服务器【间隔1min】
# @scheduler.scheduled_job('interval', minutes=1, start_date='2023-06-15 21:00:00', end_date='2023-12-31 23:00:00')
# @scheduler.scheduled_job('interval', seconds=10, start_date='2023-06-15 21:00:00', end_date='2023-12-31 23:00:00')
# def interval_task_test1():
#     print('interval task1 is run...')
#     arrs_ = _Meterstate[0]
#     msg_pub = to_bytes(arrs_)
#     topic = "U001/PUB"
#     Pub_object = Pub_Server()
#     Pub_object.mqtt_publish(topic, msg_pub)
#     print("=======0", _Meterstate)
#     print('时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#定时获取数据库数据【间隔5min】
@scheduler.scheduled_job('interval', minutes=1, start_date='2023-06-15 21:00:00', end_date='2023-12-31 23:00:00')
def cron_task_test1():
    print('cron task1 is run...')
    print('时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    msg_pub = loadJsonData()
    print(msg_pub)
    # topic = "U001/PUB"
    topic = topic_set
    Pub_object = Pub_Server()
    Pub_object.mqtt_publish(topic, msg_pub)
    print("=======1",_Meterstate)


#每10s从寄存器取一次数据
@scheduler.scheduled_job('cron', hour='0-23',second='10,20,30,40,50')
def cron_task_test2():
    print('cron task2 is run...')
    print('时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    arrs_ = _Meterstate[0]
    msg_pub = change_format(parm=['powerTotalYg', 'powerTotalWg', 'powerTotalSz', 'powerYgA', 'powerYgB', 'powerYgC', 'powerWgA', 'powerWgB',
          'powerWgC', 'energyZxyg', 'voltageA', 'voltageB', 'voltageC', 'currentA', 'currentB', 'currentC',
          'frequencyA', 'powerFactorTotal'],arr_=arrs_)
    topic =  topic_set
    # topic = "U001/PUB"
    Pub_object = Pub_Server()
    Pub_object.mqtt_publish(topic, msg_pub)
    print("=======2",_Meterstate)


# #定时获取数据库数据【间隔5min】
# @scheduler.scheduled_job('cron', hour='0-23',minute='0,15,30,45')
# def cron_task_test1():
#     print('cron task1 is run...')
#     msg_pub = loadJsonData()
#     print(msg_pub)
#     topic = "U001/PUB"
#     Pub_object = Pub_Server()
#     Pub_object.mqtt_publish(topic, msg_pub)
#     print("=======1",_Meterstate)
#     print('时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# 挂载后台管理系统
site.mount_app(app)

# 创建初始化数据库表
@app.on_event("startup")
async def startup():
    await site.db.async_run_sync(SQLModel.metadata.create_all,is_session=False)
    await auth.create_role_user(role_key='admin')

@app.on_event("startup")
async def startup():
    # 启动定时任务调度器
    scheduler.start()
    Scheduler.start()

if __name__ == '__main__':
    # import uvicorn
    # uvicorn.run(app, debug=True)

    msg_pub = loadJsonData()
    print(msg_pub)
    # topic = "U001/PUB"
    # Pub_object = Pub_Server()
    # Pub_object.mqtt_publish(topic, msg_pub)
    # print('时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #
    # print(_Meterstate)



# uvicorn BVPP_Server:app --host=0.0.0.0 --port=9999

# supervisord -c E:\Build_monitor_AI\supervisord.conf

