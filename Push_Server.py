import sys
import os
import re
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
rootPath = os.path.split(BASE_DIR)[0]
sys.path.append(rootPath)
import numpy as np
import datetime
from tools.get_conn import get_conn_db
import struct
import time
import json
from tools.logging_conf import logger
from tools.Create_xml import Xml_Producer
from tools.get_data_from_api import  Get_datas
from Config.settings import config,config0
from tools.Breakpoint_up import put_data
import threading
# from tools.get_conn import get_conn_db
from Config.template import template_send,byte_types
from tools.Modbus_tcp_con import get_modbus_tcp_data
from apscheduler.schedulers.blocking import BlockingScheduler

root_path_config = config.get('root_path_config')

root_path_log = config.get('root_path_log')

chunk_size_config = config0.get('chunk_size')

chunk_number_config = config0.get('chunk_number')

chunk_size = int(chunk_size_config)

num_chunk = int(chunk_number_config)

hostAdress0 = "192.168.0.127"
hostAdress1 = "192.168.0.128"

with open(root_path_config + '/' + 'Branch_code1.json') as f:

    data = json.load(f)

 # 对字典进行分割
def dict_chunk(dicts, size):
    new_list = []
    dict_len = len(dicts)
    # 获取分组数
    while_count = dict_len // size + 1 if dict_len % size != 0 else dict_len / size
    split_start = 0
    split_end = size
    while (while_count > 0):
        # 把字典的键放到列表中，然后根据偏移量拆分字典
        new_list.append({k: dicts[k] for k in list(dicts.keys())[split_start:split_end]})
        split_start += size
        split_end += size
        while_count -= 1
    return new_list

#获取sqlserver数据库数据

class Push_data_Sever(object):

    _Meterstate = [[] for _ in range(num_chunk)]


    def __init__(self):
        # 时间戳-年月日时分秒
        nowtime1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.t1 = ''.join([x for x in nowtime1 if x.isdigit()])

        # 建筑编号
        self.topic0 = config0.get('user')
        self.scheduler = BlockingScheduler()

    #modbus_tcp获取数据


    def get_data_from_modbustcp(self):
        nowtime1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.t1 = ''.join([x for x in nowtime1 if x.isdigit()])
        start = datetime.datetime.now()

        try:

            lst = []

            for Addr in [hostAdress0, hostAdress1]:
                lst_ = get_modbus_tcp_data(Addr)
                lst.extend(lst_)

            dict_ = {i: lst[i] for i in range(len(lst))}

            #print(dict_)

            # 数据包数量
            chunks = dict_chunk(dicts=dict_, size=chunk_size)

            for index, item in enumerate(chunks):
                print(index, item)
                #     # 设备ID-01
                Push_data_Sever._Meterstate[index].append(index + 1)
                #     # 获取当前时间(年-月-日 时:分:秒)
                Push_data_Sever._Meterstate[index].extend(
                    [int(self.t1[2:4]), int(self.t1[4:6]), int(self.t1[6:8]), int(self.t1[8:10]),
                     int(self.t1[10:12]),
                     int(self.t1[12:14])])
                # 电表数量
                Push_data_Sever._Meterstate[index].append(len(item))

                print(item)

                # # 生成字节数据# 添加电表数据
                payload = self.generate_bytes(index_=index, dict_=item)

                self.generate_xml(payload)
                Push_data_Sever._Meterstate = [[] for _ in range(num_chunk)]

                time.sleep(3)

        finally:
            table_name = 'modbus_tcp'.format(hostAdress0,hostAdress1)
            # 根据序列号判断是否执行续传检查
            end = datetime.datetime.now()
            s = (end - start).total_seconds()

            print('数据导出: %s, 耗时: %s 秒' % (table_name, s))
            logger.info('数据导出: %s, 耗时: %s 秒' % (table_name, s))

    def get_data_from_modbustcp_t(self,str):
        nowtime1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #self.t1 = ''.join([x for x in nowtime1 if x.isdigit()])
        self.t1 = str
        start = datetime.datetime.now()

        try:

            lst = []

            for Addr in [hostAdress0, hostAdress1]:
                lst_ = get_modbus_tcp_data(Addr)
                lst.extend(lst_)

            dict_ = {i: lst[i] for i in range(len(lst))}

            #print(dict_)

            # 数据包数量
            chunks = dict_chunk(dicts=dict_, size=chunk_size)

            for index, item in enumerate(chunks):
                print(index, item)
                #     # 设备ID-01
                Push_data_Sever._Meterstate[index].append(index + 1)
                #     # 获取当前时间(年-月-日 时:分:秒)
                Push_data_Sever._Meterstate[index].extend(
                    [int(self.t1[2:4]), int(self.t1[4:6]), int(self.t1[6:8]), int(self.t1[8:10]),
                     int(self.t1[10:12]),
                     int(self.t1[12:14])])
                # 电表数量
                Push_data_Sever._Meterstate[index].append(len(item))

                print(item)

                # # 生成字节数据# 添加电表数据
                payload = self.generate_bytes(index_=index, dict_=item)

                self.generate_xml(payload)
                Push_data_Sever._Meterstate = [[] for _ in range(num_chunk)]

                time.sleep(3)

        finally:
            table_name = 'modbus_tcp'.format(hostAdress0,hostAdress1)
            # 根据序列号判断是否执行续传检查
            end = datetime.datetime.now()
            s = (end - start).total_seconds()

            print('数据导出: %s, 耗时: %s 秒' % (table_name, s))
            logger.info('数据导出: %s, 耗时: %s 秒' % (table_name, s))

    # def periodic_upload(self):
    #     # 启动定时任务，每0.5分钟执行一次
    #     self.scheduler.add_job(self.get_data_from_modbustcp, 'interval', minutes=20)
    #
    #     # 手动触发一次上传
    #     print("第一次上传立即执行")
    #     self.get_data_from_modbustcp()
    #
    #     print("定时任务已启动，每30秒执行一次")
    #     self.scheduler.start()
    import os
    import re

    def periodic_upload(self):

        # 启动定时任务，每20分钟执行一次获取数据操作
        self.scheduler.add_job(self.get_data_from_modbustcp, 'interval', minutes=20)
        print("第一次上传立即执行")
        self.get_data_from_modbustcp()

        # 启动定时任务，每30分钟执行一次完整的检查和处理逻辑（包括查找缺失时间以及后续操作）
        self.scheduler.add_job(self.check_and_handle_missing_times, 'interval', minutes=60)
        self.check_and_handle_missing_times()

        print("定时任务已启动，相关操作将按设定时间间隔自动执行")
        self.scheduler.start()

    def check_and_handle_missing_times(self):
        # 获取日志文件夹下所有xml文件
        xml_files = [os.path.join(root_path_log, 'C125', f) for f in
                     os.listdir(os.path.join(root_path_log, 'C125')) if f.endswith('.xml')]
        times = []
        for xml_file in xml_files:
            match = re.search(r'(\d{4})', xml_file)
            if match:
                times.append(int(match.group(1)))

        times = sorted(times)

        # 构建完整的时间列表，从0000到2300
        all_times = ["0000", "0100", "0200", "0300", "0400", "0500", "0600", "0700", "0800", "0900", "1000", "1100",
                     "1200",
                     "1300", "1400", "1500", "1600", "1700", "1800", "1900", "2000", "2100", "2200", "2300"]

        # 从self.t1中提取当前小时对应的时间（格式化为xx00）
        current_hour = self.t1[-6:-4] + "00"
        current_index = all_times.index(current_hour)

        # 查找当前小时时间之前缺失的时间值
        missing_values = []
        for i in range(current_index):
            time_value = all_times[i]
            if int(time_value) not in times:
                missing_values.append(int(time_value))

        if missing_values:
            for missing_value in missing_values:
                missing_time_str = "{:04d}".format(missing_value)
                new_t1 = self.t1[:-6] + missing_time_str + '00'
                print("t1", self.t1)
                print('missing_time_str', missing_time_str)
                print("发现缺失，更新后的当前时间为", new_t1)
                # 假设依据更新后的时间进行后续操作，调用相关函数（这里可根据实际需求调整）
            self.get_data_from_modbustcp_t(new_t1)
        else:
            print("当前小时之前的xml文件时间前4位连续")
    #从数据库获取数据
    def get_data_from_sqlserver(self,table_name):
        """
        从sqlserver导出数据文件到本地
        """
        start = datetime.datetime.now()
        #存放键值对
        lst = []
        conn = None
        try:
            conn = get_conn_db('SOURCE')
            if conn is None:
                # 日志记录
                logger.info("获取数据库连接失败")

                raise Exception('获取数据库连接失败')

            sql="""select a.PtId,round(a.Value,1) from {0} a,(select PtId,max(RecTime) create_time from {0} where mod(PtId, 2)=0 group by PtId) b
                    where a.PtId = b.PtId and a.RecTime = b.create_time""".format(table_name)

            # sql = "SELECT CODE,round(PRESENT_VALUE,2) FROM {0} WHERE CODE LIKE '%Epd'".format(table_name)  # 数据库查询语句

            with conn.cursor() as cur:
                cur.execute(sql)
                results = cur.fetchall()
                for result in results:
                    # tuple_list = tuple([str(i) for i in list(result)][0:])
                    # print(result)
                    result = list(result)  # 元组转化为列表
                    for res in range(len(result)):
                        if isinstance(result[res], str):
                            result[res] = result[res].replace(' ', '')
                            # 解决空格问题
                    result = tuple(result)  # 列表再转换为元组
                    lst.append(result)
                # 将转换为字典
                dict_ = dict(lst)

            print(dict_)

            # 数据包数量
            chunks = dict_chunk(dicts=dict_, size=chunk_size)

            for index, item in enumerate(chunks):

                print(index, item)
                #     # 设备ID-01
                Push_data_Sever._Meterstate[index].append(index + 1)
                #     # 获取当前时间(年-月-日 时:分:秒)
                Push_data_Sever._Meterstate[index].extend(
                    [int(self.t1[2:4]), int(self.t1[4:6]), int(self.t1[6:8]), int(self.t1[8:10]),
                     int(self.t1[10:12]),
                     int(self.t1[12:14])])
                # 电表数量
                Push_data_Sever._Meterstate[index].append(len(item))

                print(item)

                # # 生成字节数据# 添加电表数据
                payload = self.generate_bytes(index_=index, dict_=item)

                self.generate_xml(payload)

                time.sleep(3)

        finally:
            table_name = 'meter'
            #根据序列号判断是否执行续传检查
            end = datetime.datetime.now()
            s = (end - start).total_seconds()

            print('数据导出: %s, 耗时: %s 秒' % (table_name, s))
            logger.info('数据导出: %s, 耗时: %s 秒' % (table_name, s))


    def get_data_from_api(self):

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

                # 数据包数量
                num_chunks = len(dict_) // chunk_size + (len(dict_) % chunk_size > 0)

                chunks = [dict_[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]


                for index, item in enumerate(chunks):
                    #     # 设备ID-01
                    Push_data_Sever._Meterstate[index].append(index + 1)
                    #     # 获取当前时间(年-月-日 时:分:秒)
                    Push_data_Sever._Meterstate[index].extend(
                        [int(self.t1[2:4]), int(self.t1[4:6]), int(self.t1[6:8]), int(self.t1[8:10]),
                         int(self.t1[10:12]),
                         int(self.t1[12:14])])
                    # 电表数量
                    Push_data_Sever._Meterstate[index].append(len(item))

                    # 生成字节数据# 添加电表数据
                    payload = self.generate_bytes(index_=index, dict_=item)

                    self.generate_xml(payload)

                    time.sleep(8)


        finally:
            table_name = 'meter'
            #根据序列号判断是否执行续传检查
            end = datetime.datetime.now()
            s = (end - start).total_seconds()

            print('数据导出: %s, 耗时: %s 秒' % (table_name, s))
            logger.info('数据导出: %s, 耗时: %s 秒' % (table_name, s))


    def generate_xml(self,payload):

        # 采集设备打包每次发送消息包含所有点表参数数据
        # 生成xml包数据
        xml_str_obj = Xml_Producer(self.topic0, payload)
        sequence = xml_str_obj.creat_xml()[2]
        try:
            xml_str_obj.publish_all_xml_files()
            print("--------------------publish_all_xml_file")
            xml_str_obj.clear_xml_files_except_0000()
            print("-------------------------all clear")
        except:
            pass


        print("更新完成,共写入%d条数据！" % sequence)

        # 记录xml数据包序列数量[一天48个包，每天检查一次]
        if sequence % 24 == 0:
            thread = threading.Thread(target=put_data, args=(f'{self.topic0}',))
            thread.start()
            # put_data(buildid=self.topic0)

   #api接口【优化发送模板】
    def generate_bytes(self,index_,dict_):

        """
        生成字节数流
        :param arr:
        :return:
        uint8 = B
        int8 = b
        uint16 = H
        int16 = h
        uint32 = I
        int32 = i
        < 小端
        > 大端

        利用template_send改写========
        """
        arr = []
        type = '>BBBBBBBB'
        data_list = []
        datain = list(data.keys())
        #print(datain)
        for key,value in dict_.items():
            #print("hhhh",key,value)
            type += template_send[0]['type']+template_send[1]['type']
            id = int(data.get(f'{key}'))
            #print(f"第{id}块表", id,key)
            if str(key) in datain:
                x = int(value * template_send[1]['mtp'])

                #print("数据",x)
                if byte_types[template_send[1]['type']]['minvalue'] <= x <= byte_types[template_send[1]['type']]['maxvalue']:
                    arr.extend([id,x])
                else:
                    arr.extend([id,byte_types[template_send[0]['type']]['default']])

            else:
                arr.extend([id,byte_types[template_send[0]['type']]['default']])

        #print(arr)

        Push_data_Sever._Meterstate[index_].extend(arr)

        data_list = Push_data_Sever._Meterstate[index_]

        to_bytes= struct.pack(type, *data_list)

        print(to_bytes)

        return to_bytes




if __name__ == '__main__':
    obj = Push_data_Sever()
    # 启动定时上传
    obj.periodic_upload()



















