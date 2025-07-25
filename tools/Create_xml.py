"""
功能：定时提取电力监控数据并打包处理成原始数据包待发送
webservers需要传入参数：建筑编号、时间、数据包
数据包参数：序列数、
"""
import os
import random
import xml.etree.ElementTree as ET
from Config.settings import config
from tools.logging_conf import logger
from Config.settings import xml_param

root_path_backup  = config.get('root_path_backup')

root_path_log = config.get('root_path_log')

#获取数据库连接
xml_params = xml_param['XML']
Number = xml_params['Split_Number']
Start = xml_params['Start']
factor =xml_params['factor']

print(root_path_backup)

from tools.subscription_model import NewsPublisher,Webservice_Subscriber
import functools
import time
import json
import struct
from tools.Reminder_service import Reminder

#处理异常的装饰器
def except_output(msg='数据生成异常'):
    """
    当数据生成，自动生成订阅webserver接口转发数据

    如果提交数据失败，本地缓存数据记录。
    再补充一个续传插件，定时检查是否有缓存数据。

    """
    # msg用于自定义函数的提示信息
    def except_execute(func):
        @functools.wraps(func)
        def execept_print(*args, **kwargs):
            try:
                u = func(*args, **kwargs)
                print("数据生成正常执行：%s" % func.__name__)

                news_publisher = NewsPublisher()
                for Subscribers in [Webservice_Subscriber]:
                    Subscribers(news_publisher)
                    print(24)
                    print("\nSubscribers", news_publisher.subscribers())

                    news_publisher.addNews(u[0],u[1])
                    print(24)
                    news_publisher.notifySubscribers()

                return u

            except Exception as e:
                print("接口异常，调用失败：%s" % e.__doc__)
                info={f"{u[0]}":f"{u[1]}"}
                print(info)
                logger.info("接口异常，调用失败")

                #微信提醒服务
                # Reminder()

                def backup_save(filename, record):  # filename为写入txt文件的路径，record为要写入json.
                    try:
                        with open(filename, 'a+', encoding='utf-8') as f:  # 覆盖方式
                            f.write(json.dumps(record)+'\n')

                    except IOError as e:
                        print(e)

                filename = root_path_backup +'/' + "{0}_backup_record.txt".format(
                    u[0])

                os.makedirs(os.path.dirname(filename), exist_ok=True)

                backup_save(filename=filename,record=u[1])

                return u

        return execept_print
    return except_execute


# 文件夹本地存储
def text_save(filename, record):  # filename为写入txt文件的路径，record为要写入json.
    try:
        with open(filename, 'w', encoding='gbk') as f:  # 覆盖方式
            f.write(json.dumps(record))
            f.close()
    except IOError as e:
        print(e)

class Xml_Producer(object):
    """
    订阅MQTT服务器数据，解析打包
    生产xml数据包实时推送到消息队列【实时发送数据包】

    building_id:W001/GPUB,通过传入主题，映射字典获取
    gateway_id：采集设备ID
    功能：字节数据还原，判断数据是否异常并打包，有功电能递增，
    如果电能数据变化异常，则用上一个时刻数据替换。
    """
    _servers = {'gateway_id':0,'sequence':0, 'data_record': 0, 'sample_time':0,'update_time':0}

    ##还原解析接收数据流字节
    def __init__(self,topic=None,payload=None):
        """
        #订阅数据解析还原【规整固定数据格式】
        #时间戳 (23, 2, 28, 14, 28, 20)
        """
        self.building_id = topic
        self.gateway_id = payload[0]
        print("采集设备ID", payload[0])
        self.tuple_time = struct.unpack('>BBBBBB', payload[1:7])
        sample_time0 = f'20{self.tuple_time[0]}{self.str_fill(self.tuple_time[1])}' \
                      f'{self.str_fill(self.tuple_time[2])}{self.str_fill(self.tuple_time[3])}' \
                      f'{self.str_fill(self.tuple_time[4])}{self.str_fill(self.tuple_time[5])}'
        print("时间", sample_time0)
        self.sample_time = f'20{self.tuple_time[0]}{self.str_fill(self.tuple_time[1])}' \
                      f'{self.str_fill(self.tuple_time[2])}{self.str_fill(self.tuple_time[3])}' \
                      f'0000'
        #self.sample_time = '20241130090000'
        print("整点时间", sample_time0)

        self.Meter_number = struct.unpack('>B', payload[7:8])[0]
        print("电表数量", self.Meter_number)

        self.Meter_record = struct.unpack('>' + 'Hi' * self.Meter_number, payload[8:])

        #系数
        self.factor = factor


        print("电表数据记录", self.Meter_record)

        # 发送xml模板数据

    @except_output(msg='数据生成异常')
    def creat_xml(self):
        # 初始化数据记录
        self.filename = root_path_log + '/' + f"{self.building_id}/data_record_gateway{self.gateway_id}.txt"

        if os.path.exists(self.filename):
            # 数据本地存储【数据更新】
            print("记录存在，更新记录")
            sequence = self.xml_sequence()
            self.backup_record(sequence=sequence)


            xml_str = self.xml_encode(seq=sequence, error=192, coding='', parser='yes')


        else:

            print("记录不存在，初始化...")
            # 创建文件夹
            # os.makedirs(root_path_log + '/' + f"{self.building_id}")
            self.text_create(msg=' ')
            # 生成空文件
            self.init_record()

            sequence = self.xml_sequence()
            self.backup_record(sequence=sequence)

            xml_str = self.xml_encode(seq=sequence, error=192, coding='', parser='yes')

        return self.building_id,xml_str,sequence

    # 函数中的name是新建文件的名字，msg是写入的内容，类型为str类型，可任意传参
    def text_create(self,msg):
        full_path = self.filename
        file = open(full_path, 'w')  # w 的含义为可进行读写
        file.write(msg)  # file.write()为写入指令
        file.close()

    #填充固定位数
    def str_fill(self,k_time):
        str_time = str(k_time).zfill(2)
        return str_time

    def str_fill_code(self,code):
        str_code =self.building_id + str(code).zfill(3)
        return str_code

    # 回调更新本地记录【订阅后本地保存】
    def record(func):
        def Server_record(self,*args,**kwargs):
            v = func(self,*args,**kwargs)
            text_save(filename= root_path_log + '/' + "{0}/data_record_gateway{1}.txt".format(
                self.building_id,self.gateway_id),record=Xml_Producer._servers)
            print("最新记录更新成功")
            return v
        return Server_record

    #读取最新数据【定时调用接口读取数据并发送】
    def record_log(self):
        # 读取原设定参数
        root_path = root_path_log +'/' + f'{self.building_id}'
        f_path = root_path + '/' + f'data_record_gateway{self.gateway_id}.txt'
        try:
            with open(f_path, 'r') as f:
                temp = f.read()
                if temp:
                    data = json.loads(temp)
                    print(data)
        except IOError as e:
            print(e)

    def init_record(self):

        ini_data_record = {
            'gateway_id': 0,
            'sequence': 0,
            'data_record': 0,
            'sample_time': 0,
            'update_time': 0
        }

        # 初始化记录
        root_path =root_path_log +'/' + f'{self.building_id}'
        f_path = root_path + '/' + f'data_record_gateway{self.gateway_id}.txt'

        with open(f_path, 'w') as f:
            f.write(json.dumps(ini_data_record))

    @record
    def backup_record(self,sequence):
        """
        #读取本地离线缓存数据
        """
        # 最新记录更新
        self._servers['gateway_id'] = self.gateway_id
        self._servers['sequence'] = sequence
        self._servers['data_record'] = self.Meter_record
        self._servers['sample_time'] = self.sample_time
        self._servers['update_time'] = f"{int(time.time())}"
        # print(self._servers)
        return self._servers

    #判断采集设备是否离线【离线发送缓存数据包】-------单独出离线报警功能
    def status_code(self,val):
        """
        error属性:该功能出现错误的状态码，192表示没有错误,0表示计量装置离线
        """
        #读取最新数据记录
        # 读取最新数据记录
        if val >= 0 :
            error = 192
        else:
            error = 0

        return error

    def xml_sequence(self):
        """
        sequence元素:采集器向服务器发送数据的序号,递增
        """
        #读取最新序列数据
        with open(self.filename, 'r') as f:
            temp = f.read()
            data = json.loads(temp)
        sequence = int(data["sequence"])+1

        return sequence

    def split_(self,str_record,n):
        for i in range(0, len(str_record), n):
            yield list(str_record[i:i + n])


    def xml_encode(self,seq,error,coding='',parser='yes'):
        """
        #按点表模板生成数据【考虑为不同建筑配置不同的xml数据模板】
        """
        # 标记common节点开始标签
        xmlItem = ['<?xml version="1.0" encoding="UTF-8"?>''<root>''<common>']

        str_common = f"<building_id>440300{self.building_id}</building_id><gateway_id>{self.str_fill(self.gateway_id)}</gateway_id><type>report</type>"

        xmlItem.append(str_common)

        # 标记data节点结束标签
        xmlItem.append('</common>')

        # 标记data节点开始标签
        data_Item = ['<data operation="report">']

        str_data = """<sequence>{0}</sequence><parser>{1}</parser><time>{2}</time>""".format(
            seq, parser, self.sample_time)

        data_Item.append(str_data)

        print("========2023",self.Meter_record)

        print(Number,Start)

        # 【逐条记录迭代生成】
        for record in self.split_(str_record=self.Meter_record, n=Number):
            """
            备注：预留位置12位【建筑编号+三位设备ID】-1090；其他参数后期定义完善
            AB线电压:8B6
            BC线电压:9B6
            CA线电压:10B6
            A相电压:11B6
            B相电压:12B6
            C相电压:13B6
            A相电流:21B6
            B相电流:22B6
            C相电流:23B6
            视在功率::32B6
            有功功率：31B6
            无功功率: 11B6
            电量读数：1090
            """
            record = record
            #print("设备采集参数记录", record)
            #电表参数【根据情况生成参数】参数代号，可配置项，默认全部参数上传
            Meter_Parameters = ['1090']
            # Meter_Parameters = ['31B6', '11B6', '1090']
            #支路编号
            code = record[0]
            #参数值，与参数编码对应
            value = record[Start:]
            # value = record[13:]
            str_meter = [f'<meter id="{2000+code}" name="{self.str_fill_code(code)}" conn="conn">']

            for j in range(len(Meter_Parameters)):
                error = self.status_code(value[0])
                if value[0]<0:
                    #输入替换的模板：给行中每个字段加固定xml格式
                    str_function = f"""<function id="{j}" name="{self.str_fill_code(code)}-{Meter_Parameters[j]}" coding="{coding}" error="{error}" sample_time="{self.sample_time}"> </function>"""
                    str_meter.append(str_function)
                else:
                    #输入替换的模板：给行中每个字段加固定xml格式
                    str_function = f"""<function id="{j}" name="{self.str_fill_code(code)}-{Meter_Parameters[j]}" coding="{coding}" error="{error}" sample_time="{self.sample_time}">{round(value[j]*self.factor/10.0,2)}</function>"""
                    str_meter.append(str_function)
            str_meter.append('</meter>')
            data_Item.extend(str_meter)

        # 标记data节点结束标签
        data_Item.append('</data>''</root>')
        xmlItem.extend(data_Item)

        # # 返回字符串
        xml_str = '\n'.join(xmlItem)  # list 更新成str

        self.write_xml(xml_str)
        return xml_str

    def write_xml(self,xml_str):
        #格式化
        # xmlstr = xml_str.encode('utf-8')
        import xml.dom.minidom
        xml = xml.dom.minidom.parseString(xml_str)
        xml_pretty_str = xml.toprettyxml(indent='\t')
        # print(xml_pretty_str)
        with open(root_path_log + fr"\{self.building_id}\last_time_xml_record.xml", 'w') as xmlFile:
            # 写数据
            xmlFile.write(xml_pretty_str)
        with open(root_path_log + fr"\{self.building_id}\{self.sample_time[-6:-2]}time_xml_record.xml", 'w+') as xmlFile:
            # 写数据
            xmlFile.write(xml_pretty_str)

    # 提取xml数据
    def read_xml(self,xmlFileName):
        with open(xmlFileName, 'r') as xml_file:
            xml_text =xml_file.read()
            #print("xml", xml_text)

    def publish_all_xml_files(self):
        """
        遍历root_path_log文件夹下的所有xml文件，并逐个发布
        """
        xml_files = [os.path.join(root_path_log, self.building_id,f) for f in os.listdir(os.path.join(root_path_log, self.building_id)) if f.endswith('.xml')]
        #print(xml_files)
        news_publisher = NewsPublisher()
        for Subscribers in [Webservice_Subscriber]:
            Subscribers(news_publisher)
            #print(Subscribers)
        ccc = 1
        for xml_file in xml_files:
            with open(xml_file, 'r') as file:
                xml_content = file.read()
                #building_id = os.path.basename(xml_file).split('.')[0].split('_')[0]  # 从文件名提取building_id，可根据实际情况调整提取逻辑
                building_id = self.building_id
                news_publisher.addNews(building_id, xml_content)
                news_publisher.notifySubscribers()
                print(f"第{ccc}个上传++++++++++++++++++++++成功")
                ccc += 1
    # def publish_all_xml_files(self):
    #     """
    #     遍历root_path_log文件夹下的所有xml文件，并逐个发布，同时处理缺失时间相关的xml复制和修改
    #     """
    #     xml_files = [os.path.join(root_path_log, self.building_id, f) for f in os.listdir(
    #         os.path.join(root_path_log, self.building_id)) if f.endswith('.xml')]
    #     existing_times = []
    #
    #     # 第一步：遍历所有xml文件，提取已有的时间
    #     for xml_file in xml_files:
    #         with open(xml_file, 'r') as file:
    #             xml_content = file.read()
    #             root = ET.fromstring(xml_content)
    #             meter_conns = root.findall('.//meter_conn')
    #             for meter_conn in meter_conns:
    #                 sample_time = meter_conn.find('function').attrib['sample_time']
    #                 existing_times.append(sample_time)
    #             # 检查common元素下的time元素
    #             common_time = root.find('.//common/time')
    #             if common_time is not None:
    #                 existing_times.append(common_time.text)
    #
    #     # 获取当前的sampletime
    #     current_sampletime = self.sample_time
    #
    #     # 计算当前sampletime之前的缺失时间
    #     existing_times = [time for time in existing_times if time <= current_sampletime]
    #     all_possible_times = sorted(existing_times)
    #     missing_times = []
    #     found_current = False
    #     for time in all_possible_times:
    #         if time == current_sampletime:
    #             found_current = True
    #         elif not found_current:
    #             missing_times.append(time)
    #
    #     # 打印缺失时间
    #     print("缺失时间有：", missing_times)
    #
    #     news_publisher = NewsPublisher()
    #     for Subscribers in [Webservice_Subscriber]:
    #         Subscribers(news_publisher)
    #
    #     ccc = 1
    #     for xml_file in xml_files:
    #         with open(xml_file, 'r') as file:
    #             xml_content = file.read()
    #             building_id = self.building_id
    #             news_publisher.addNews(building_id, xml_content)
    #             news_publisher.notifySubscribers()
    #             print(f"第{ccc}个上传++++++++++++++++++++++成功")
    #             ccc += 1
    #
    #     # 第二步：对于每个缺失的时间，复制随机一个xml并修改时间相关内容
    #     for missing_time in missing_times:
    #         # 随机选择一个xml文件
    #         random_xml_file = random.choice(xml_files)
    #         with open(random_xml_file, 'r') as file:
    #             xml_content = file.read()
    #             root = ET.fromstring(xml_content)
    #             meter_conns = root.findall('.//meter_conn')
    #             new_meter_conn = ET.Element('meter_conn')
    #             for meter_conn in meter_conns:
    #                 new_child = ET.Element(meter_conn.tag)
    #                 for k, v in meter_conn.attrib.items():
    #                     if 'sample_time' in k:
    #                         new_child.attrib[k] = missing_time
    #                     else:
    #                         new_child.attrib[k] = v
    #                 new_meter_conn.append(new_child)
    #             root.append(new_meter_conn)
    #             # 修改common元素下的time元素
    #             common_time = root.find('.//common/time')
    #             if common_time is not None:
    #                 common_time.text = missing_time
    #
    #             # 将修改后的xml内容重新格式化并保存
    #             import xml.dom.minidom
    #             xml = xml.dom.minidom.parseString(ET.tostring(root, encoding='utf-8').decode('utf-8'))
    #             xml_pretty_str = xml.toprettyxml(indent='\t')
    #             with open(root_path_log + fr"\{self.building_id}\{missing_time}time_xml_record.xml", 'w') as xmlFile:
    #                 xmlFile.write(xml_pretty_str)

    def clear_xml_files_except_0000(self):
        if self.sample_time[-6:-2] == "0000":
            xml_files = [os.path.join(root_path_log, self.building_id,f) for f in os.listdir(os.path.join(root_path_log, self.building_id)) if f.endswith('.xml')]
            for xml_file in xml_files:
                file_name = os.path.basename(xml_file)
                if "0000" not in file_name:
                    os.remove(xml_file)


# if __name__ == '__main__':
#     obj = Xml_Producer()


