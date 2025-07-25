
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import struct
import pandas as pd
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

#32位有符号数据，低16位前，高16位后
#2号配电房
def ModbusTcp_server2(hostAdress,portName,slaveAdress):
    try:
        result = tuple()

        data_506 = tuple()
        data_507 = tuple()


        master_506 = modbus_tcp.TcpMaster(host=hostAdress, port=506)
        master_507 = modbus_tcp.TcpMaster(host=hostAdress, port=507)
        # master.set_timeout(50.0)
        logger.info("connected")

        register_506 = [30000, 30026, 30052, 30078, 30110, 30142, 30174, 30206, 30238, 30270,
            30302, 30334, 30366, 30398, 30430, 30462, 30494, 30526, 30558, 30590,
            30622, 30654, 30686, 30718, 30750, 30782, 30814, 30846, 30878, 30910,
            30942, 30974, 31006, 31038, 31070, 31102, 31134, 31166, 31198, 31230,
            31262, 31294, 31326, 31358, 31390, 31422, 31454, 31486, 31518, 31550,
            31582, 31614, 31646, 31678, 31710, 31742, 31768, 31794, 31820, 31852,
            31884, 31916, 31948, 31980, 32012, 32044, 32076, 32108, 32140, 32172,
            32204, 32236, 32268, 32300, 32332, 32364, 32396, 32428, 32460, 32492,
            32524, 32556, 32588, 32620, 32652, 32684, 32716, 32748, 32780, 32806,
            32832, 32858, 32884, 32916, 32948, 32980, 33012, 33044, 33076, 33108,
            33140, 33172, 33204, 33236, 33268, 33300, 33332, 33364, 33396, 33428,
            33460, 33492, 33524, 33556]
        register_507 = [30000, 30032, 30064, 30096, 30128, 30160, 30192, 30224, 30256, 30288,
            30320, 30352, 30384, 30416, 30448, 30480, 30506, 30532, 30558, 30590,
            30622, 30654, 30686, 30718, 30750, 30782, 30814, 30846, 30878, 30910,
            30942, 30974, 31006, 31038, 31070, 31102, 31134, 31166, 31198, 31230,
            31262, 31294, 31326, 31358, 31390, 31422, 31454, 31486, 31518, 31550,
            31582, 31614, 31646, 31678]
        register_504 = [
            30000, 30026, 30052, 30078, 30104, 30136, 30168, 30200, 30232, 30264,
            30296, 30328, 30360, 30392, 30424, 30456, 30488, 30520, 30552, 30584,
            30616, 30648, 30680, 30712, 30744, 30776, 30808, 30840, 30872, 30904,
            30936, 30968, 31000, 31032, 31064, 31096, 31128, 31160, 31192, 31224,
            31256, 31288, 31314, 31340, 31366, 31398, 31430, 31462, 31494, 31526,
            31558, 31590, 31622
        ]
        register_505 = [
            30000, 30032, 30064, 30096, 30128, 30160, 30192, 30224, 30256, 30288,
            30320, 30352, 30384, 30416, 30448, 30480, 30512, 30544, 30576, 30608,
            30640, 30672, 30704, 30736, 30768, 30800, 30832
        ]
        try:
            #指令格式：机号 功能代码 起始地址 结束地址【读取寄存器数据】
            for v in register_506:
                data6 = master_506.execute(slaveAdress, cst.READ_HOLDING_REGISTERS, v, 2)
                data_506 = data_506.__add__(data6)
            # data_502 = master_502.execute(slaveAdress, cst.READ_HOLDING_REGISTERS, 30000, 116)
            for v in register_507:
                data7 = master_507.execute(slaveAdress, cst.READ_HOLDING_REGISTERS, v, 2)
                data_507 = data_507.__add__(data7)
            # data_503 = master_503.execute(slaveAdress, cst.READ_HOLDING_REGISTERS, 30000, 60)

            # data_505 = master_505.execute(slaveAdress, cst.READ_HOLDING_REGISTERS, 30000, 54)
        except:
            data0 = [[32767] * 168]
            data0 = tuple(data0[0])
            result = result.__add__(data0)
            print("nowlan")
            return result

        for i in [data_506, data_507]:
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

        register_1 = [
            30000, 30026, 30052, 30078, 30104, 30130, 30156, 30188, 30220, 30252,
            30284, 30316, 30348, 30380, 30412, 30444, 30476, 30508, 30540, 30572,
            30604, 30636, 30668, 30700, 30732, 30764, 30790, 30816, 30848, 30880,
            30912, 30944, 30976, 31008, 31040, 31072, 31104, 31136, 31168, 31200,
            31232, 31264, 31296, 31328, 31360, 31392, 31424, 31456, 31482, 31508,
            31534, 31560, 31586, 31618, 31650, 31682, 31714, 31746, 31778, 31810,
            31842, 31874, 31906, 31938, 31970, 32002, 32034, 32066, 32098, 32130,
            32162, 32194, 32226, 32258, 32290, 32322, 32354, 32386, 32418, 32450,
            32482, 32514,32546,32578,32610,32642,32674]
        try:
            #指令格式：机号 功能代码 起始地址 结束地址【读取寄存器数据】
            for v in register_1:
                data0 = master.execute(slaveAdress, cst.READ_HOLDING_REGISTERS, v, 2)
                result = result.__add__(data0)

        except:
            data0 = [[32767] * 82]
            data0 = tuple(data0[0])
            result = result.__add__(data0)
            return result

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

        for i in range(round(len(data_1) / 2)):
            s = ReadFloat2(data_1[i * 2:i * 2 + 2], reverse=False)
            # s = data[i * 2 + 1]
            k_V_1[i] = round(s * 0.01, 2)

    elif hostAdress=="192.168.0.128":

        data_2 = ModbusTcp_server2(hostAdress, portName, slaveAdress)

        for j in range(round(len(data_2) / 2)):
            s = ReadFloat2(data_2[j * 2:j * 2 + 2], reverse=False)
            # s = data[i * 2 + 1]
            k_V_2[j] = round(s * 0.01, 2)



    # #点表数据
    k_V = KV | k_V_1 | k_V_2
    print(k_V.values())
    value = list(k_V.values())

    return value

#
# if __name__ == '__main__':
#
#     hostAdress0 = "162.168.8.51"
#     hostAdress1 = "162.168.8.52"
#
#     lst = []
#
#     for Addr in [hostAdress0,hostAdress1]:
#         lst_ = get_modbus_tcp_data(Addr)
#         lst.extend(lst_)
#
#     new_dict = {i: lst[i] for i in range(len(lst))}

    # print(new_dict)

