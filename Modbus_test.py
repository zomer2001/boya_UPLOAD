import time
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import struct
import pandas as pd
import sys
import os
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

chunk_size_config = config0.get('chunk_size')

chunk_number_config = config0.get('chunk_number')

chunk_size = int(chunk_size_config)

num_chunk = int(chunk_number_config)

hostAdress1 = "192.168.0.127"
hostAdress2 = "192.168.0.128"
logger = modbus_tk.utils.create_logger("console")

def ReadFloat2(*args, reverse=True):
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
    :param args:
    :param reverse:
    :return:
    """
    # 解析浮点数
    try:
        for i ,j in args:
            if i == 32767:
                return -10000
            else:
                return i*65536+j
    except:
        logger.warning("Error 2000: Failed When dec2float!" )
        a = -88.8
        return a
        pass

def ReadFloat(*args, reverse=True):
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
    :param args:
    :param reverse:
    :return:
    """
    # 解析浮点数
    try:
        for i, j in args:
            i, j = '%04x' % i, '%04x' % j
        if reverse:
            v = i + j
        else:
            v = j + i
        y_bytes = bytes.fromhex(v)
        y = struct.unpack('>i', y_bytes)[0]
        y = round(y, 6)
        return y
    except:
        logger.warning("Error 2000: Failed When dec2float!" )
        a = -88.8
        return a
        pass

def ReadFloat_2(*args, reverse=True):
    """
    从四个连续的Modbus寄存器中解析浮点数。
    :param registers: 一个包含四个int16值的列表或元组，代表四个连续的Modbus寄存器。
    :param reverse: 是否需要反转字节序，默认为False，即保持大端格式。
    :return: 解析后的浮点数。
    """
    try:
        # 将寄存器值组合成一个64位的十六进制字符串
        hex_str = ''.join(f'{i:04x}' for i in args)

        # 将十六进制字符串转换为字节
        y_bytes = bytes.fromhex(hex_str)

        # 如果需要反转字节序
        if reverse:
            y_bytes = y_bytes[::-1]

        # 解包为8字节的浮点数（double）
        # '>d' 表示大端格式的双精度浮点数
        y = struct.unpack('>d', y_bytes)[0]

        return y
    except Exception as e:
        logger.warning(f"Error 2000: Failed When converting registers to float! {e}")
        return -88.8

# 32位有符号数据，低16位前，高16位后
# 配电房数据处理
def ModbusTcp_server2(hostAdress,portName,slaveAdress):
    try:
        result = tuple()


        master_506 = modbus_tcp.TcpMaster(host=hostAdress, port=506)
        master_507 = modbus_tcp.TcpMaster(host=hostAdress, port=507)
        # master.set_timeout(50.0)
        logger.info("connected")

        register_6 = [30000, 30026, 30052, 30078, 30110, 30142, 30174, 30206, 30238, 30270, 30302, 30334, 30366, 30398, 30430, 30462, 30494, 30526, 30558, 30590, 30622, 30654, 30686, 30718, 30750, 30782, 30814, 30846, 30878, 30910, 30942, 30974, 31006, 31038, 31070, 31102, 31134, 31166, 31198, 31230, 31262, 31294, 31326, 31358, 31390, 31422, 31454, 31486, 31518, 31550, 31582, 31614, 31646, 31678, 31710, 31742, 31768, 31794, 31820, 31852, 31884, 31916, 31948, 31980, 32012, 32044, 32076, 32108, 32140, 32172, 32204, 32236, 32268, 32300, 32332, 32364, 32396, 32428, 32460, 32492, 32524, 32556, 32588, 32620, 32652, 32684, 32716, 32748, 32780, 32806, 32832, 32858, 32884, 32916, 32948, 32980, 33012, 33044, 33076, 33108, 33140, 33172, 33204, 33236, 33268, 33300, 33332, 33364, 33396, 33428, 33460, 33492, 33524, 33556]
        # 指令格式：机号 功能代码 起始地址 结束地址【读取寄存器数据】
        for v in register_6:
            data_506 = master_506.execute(slaveAdress, cst.READ_HOLDING_REGISTERS, v, 2)
        # data_502 = master_502.execute(slaveAdress, cst.READ_HOLDING_REGISTERS, 30000, 116)
            print("data_502=============", data_506)
        data_503 = master_503.execute(slaveAdress, cst.READ_HOLDING_REGISTERS, 30000, 60)
        print("data_503=============", data_503)
        data_504 = master_504.execute(slaveAdress, cst.READ_HOLDING_REGISTERS, 30000, 106)
        print("data_504=============", data_504)
        data_505 = master_505.execute(slaveAdress, cst.READ_HOLDING_REGISTERS, 30000, 54)
        print("data_505=============", data_505)
        for i in [data_502, data_503, data_504, data_505]:
            result = result.__add__(i)
    except modbus_tk.modbus.ModbusError as e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))
    print('result', result)
    return result


#1号配电房
def ModbusTcp_server1(hostAdress,portName,slaveAdress):
    try:
        result = tuple()

        master = modbus_tcp.TcpMaster(host=hostAdress, port=portName)
        master.set_timeout(50.0)
        logger.info("connected")

        # register_1 = [
        #     30000, 30026, 30052, 30078, 30104, 30130, 30156, 30188, 30220, 30252,
        #     30284, 30316, 30348, 30380, 30412, 30444, 30476, 30508, 30540, 30572,
        #     30604, 30636, 30668, 30700, 30732, 30764, 30790, 30816, 30848, 30880,
        #     30912, 30944, 30976, 31008, 31040, 31072, 31104, 31136, 31168, 31200,
        #     31232, 31264, 31296, 31328, 31360, 31392, 31424, 31456, 31482, 31508,
        #     31534, 31560, 31586, 31618, 31650, 31682, 31714, 31746, 31778, 31810,
        #     31842, 31874, 31906, 31938, 31970, 32002, 32034, 32066, 32098, 32130,
        #     32162, 32194, 32226, 32258, 32290, 32322, 32354, 32386, 32418, 32450,
        #     32482, 32514]
        register_1 = [
            30000, 30026, 30052, 30078, 30104, 30130, 30156, 30188, 30220, 30252,
            30284, 30316, 30348, 30380, 30412, 30444, 30476, 30508, 30540, 30572,
            30604, 30636, 30668, 30700, 30732, 30764, 30790, 30816, 30848, 30880,
            30912, 30944, 30976, 31008, 31040, 31072, 31104, 31136, 31168, 31200,
            31232, 31264, 31296, 31328, 31360, 31392, 31424, 31456, 31482, 31508,
            31534, 31560, 31586, 31618, 31650, 31682, 31714, 31746, 31778, 31810,
            31842, 31874, 31906, 31938, 31970, 32002, 32034, 32066, 32098, 32130,
            32162, 32194, 32226, 32258, 32290, 32322, 32354, 32386, 32418, 32450,
            32482, 32514, 32546, 32578, 32610, 32642, 32674]

        #指令格式：机号 功能代码 起始地址 结束地址【读取寄存器数据】
        for v in register_1:
            data0 = master.execute(slaveAdress, cst.READ_HOLDING_REGISTERS, v, 2)
            result = result.__add__(data0)

    except modbus_tk.modbus.ModbusError as e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))


    return result

def get_modbus_tcp_data(hostAdress):
    # 端口号码
    portName = 502
    # 从站的站号
    slaveAdress = 1
    k_V_2 = {}
    k_V_1 = {}
    KV = {}
    if hostAdress=="192.168.0.127":

        data_1 = ModbusTcp_server1(hostAdress, portName, slaveAdress)
        #print(data_1)

        for i in range(round(len(data_1) / 2)):
            s = ReadFloat2(data_1[i * 2:i * 2 + 2], reverse=False)
            # s = data[i * 2 + 1]
            k_V_1[i] = round(s * 0.01, 2)
            print(s)

    elif hostAdress=="192.168.0.128":

        data_2 = ModbusTcp_server2(hostAdress, portName, slaveAdress)

        for j in range(round(len(data_2) / 2)):
            s = ReadFloat2(data_2[j * 2:j * 2 + 2], reverse=False)
            # s = data[i * 2 + 1]
            k_V_2[j] = round(s * 0.01, 2)



    # #点表数据
    k_V = KV | k_V_1 | k_V_2
    #print(k_V.values())
    value = list(k_V.values())

    return value


def get_data_from_modbustcp():


    lst = []

    for Addr in [ hostAdress1,hostAdress2]:
        lst_ = get_modbus_tcp_data(Addr)
        lst.extend(lst_)

    dict_ = {i: lst[i] for i in range(len(lst))}

    #print(dict_)


if __name__ == '__main__':
    # init 初始化信息
    # 162.168.8.120
    # 1号配电房 192.168.0.127
    # 2号配电房 192.168.0.128
    # 从站的IP地址502
    # hostAdress = "162.168.8.52"
    #while True:
 #    hostAdress = "192.168.0.127"
 #    # 端口号码
 #    portName = 502
 #    # 从站的站号
 #    slaveAdress = 1
 #
 # # 每2分钟存数据为Excel表格
 #    data = ModbusTcp_server1(hostAdress, portName, slaveAdress)
 #    k_V = {}
 #    for i in range(round(len(data)/2)):
 #
 #        s = ReadFloat2(data[i * 2:i * 2 + 2], reverse=False)
 #        #s = data[i * 2 + 1]
 #        #print(s)
 #        k_V[i] = round(s*0.01, 1)
 #        # #点表数据
 #        print(k_V)
 #        #print(data)
 #
 #    # value = list(k_V.values())
 #    # print("配电房数据", value)
 #    key = list(k_V.keys())
 #    value = list(k_V.values())
 #    result_excel = pd.DataFrame()
 #    result_excel["点号"] = key
 #    result_excel["遥测值"] = value
 #    print(value)
 #    # 写入excel
 #    result_excel.to_excel(r"C:\Users\Administrator\Desktop\数据上传\test\配电房数据.xlsx")
    get_data_from_modbustcp()
