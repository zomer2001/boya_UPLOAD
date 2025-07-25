
# 【BVPP】发送数据模板
# template_send = {
#         0: {'name': 'powerTotalYg', 'type': 'H', 'mtp': 1,'comment': '总有功功率'},
#         1: {'name': 'powerTotalWg', 'type': 'H', 'mtp': 1,'comment': '总无功功率'},
#         2: {'name': 'powerTotalSz', 'type': 'H', 'mtp': 1,'comment': '总视在功率'},
#         3: {'name': 'powerYgA', 'type': 'H', 'mtp': 1,'comment': 'A相有功功率'},
#         4: {'name': 'powerYgB', 'type': 'H', 'mtp': 1,'comment': 'B相有功功率'},
#         5: {'name': 'powerYgC', 'type': 'H', 'mtp': 1,'comment': 'C相有功功率'},
#         6: {'name': 'powerWgA', 'type': 'H', 'mtp': 1,'comment': 'A相无功功率'},
#         7: {'name': 'powerWgB', 'type': 'H', 'mtp': 1,'comment': 'B相无功功率'},
#         8: {'name': 'powerWgC', 'type': 'H', 'mtp': 1,'comment': 'C相无功功率'},
#         9: {'name': 'energyZxyg', 'type': 'H', 'mtp': 1,'comment': '计算电量'},
#         10: {'name': 'voltageA', 'type': 'H', 'mtp': 1,'comment': 'A相电压'},
#         11: {'name': 'voltageB', 'type': 'H', 'mtp': 1,'comment': 'B相电压'},
#         12: {'name': 'voltageC', 'type': 'H', 'mtp': 1,'comment': 'C相电压'},
#         13: {'name': 'currentA', 'type': 'H', 'mtp': 1,'comment': 'A相电流'},
#         14: {'name': 'currentB', 'type': 'H', 'mtp': 1,'comment': 'B相电流'},
#         15: {'name': 'currentC', 'type': 'H', 'mtp': 1,'comment': 'C相电流'},
#         16: {'name': 'frequencyA', 'type': 'H', 'mtp': 1,'comment': '频率'},
#         17: {'name': 'powerFactorTotal', 'type': 'b', 'mtp': 1,'comment': '功率因素'},
#     }

#数据上传
template_send = {
        0: {'id': 'address', 'type': 'H', 'mtp': 1,'comment': '电表ID'},
        1: {'name': 'energyZxyg', 'type': 'i', 'mtp': 10,'comment': '计算电量'},
    }

# 字节类型关联参数
byte_types = {
        'B': {'length': 1, 'default': 0, 'maxvalue': 255, 'minvalue': 0},
        'b': {'length': 1, 'default': 0, 'maxvalue': 127, 'minvalue': -127},
        'H': {'length': 2, 'default': 0, 'maxvalue': 256*256-1, 'minvalue': 0},
        'h': {'length': 2, 'default': 0, 'maxvalue': 256*128-1, 'minvalue': -256*128+1},
        'I': {'length': 4, 'default': 0, 'maxvalue': 256*256*256*256-1, 'minvalue': 0},
        'i': {'length': 4, 'default': 0, 'maxvalue': 256*256*256*128-1, 'minvalue': -256*256*256*128+1},
    }


# 接受数据模板[控制命令参数]
# template_recv = {
#         0: {'address': [50, 51], 'name': 'control_mode', 'type': 'B', 'mtp': 1, 'maxvalue': 4, 'minvalue': 0},
#         1: {'address': [51, 55], 'name': 'target_power', 'type': 'i', 'mtp': 10, 'maxvalue': 10000, 'minvalue': -10000},
#         2: {'address': [55, 56], 'name': 'Factor', 'type': 'B', 'mtp': 100, 'maxvalue': 100, 'minvalue': 0},
#         3: {'address': [56, 57], 'name': 'priority_raise', 'type': 'B', 'mtp': 1, 'maxvalue': 3, 'minvalue': 0},
#         4: {'address': [57, 58], 'name': 'priority_down', 'type': 'B', 'mtp': 1, 'maxvalue': 3, 'minvalue': 0},
#         5: {'address': [58, 60], 'name': 'signal', 'type': 'H', 'mtp': 10, 'maxvalue': 10000, 'minvalue': 0},
#     }

# self.Meter_record = struct.unpack('>' + 'HHHHHHHHHHHHHI' * self.Meter_number, payload[8:])
#订阅解析
template_recv  = {
        0: {'address':[0,2],'name': 'powerTotalYg', 'type': 'H', 'mtp': 1,'comment': '总有功功率','maxvalue': 256*256-1, 'minvalue': 0},
        1: {'address':[2,4],'name': 'powerTotalWg', 'type': 'H', 'mtp': 1,'comment': '总无功功率','maxvalue': 256*256-1, 'minvalue': 0},
        2: {'address':[4,6],'name': 'powerTotalSz', 'type': 'H', 'mtp': 1,'comment': '总视在功率','maxvalue': 256*256-1, 'minvalue': 0},
        3: {'address':[6,8],'name': 'powerYgA', 'type': 'H', 'mtp': 1,'comment': 'A相有功功率','maxvalue': 256*256-1, 'minvalue': 0},
        4: {'address':[8,10],'name': 'powerYgB', 'type': 'H', 'mtp': 1,'comment': 'B相有功功率','maxvalue': 256*256-1, 'minvalue': 0},
        5: {'address':[10,12],'name': 'powerYgC', 'type': 'H', 'mtp': 1,'comment': 'C相有功功率','maxvalue': 256*256-1, 'minvalue': 0},
        6: {'address':[12,14],'name': 'powerWgA', 'type': 'H', 'mtp': 1,'comment': 'A相无功功率','maxvalue': 256*256-1, 'minvalue': 0},
        7: {'address':[14,16],'name': 'powerWgB', 'type': 'H', 'mtp': 1,'comment': 'B相无功功率','maxvalue': 256*256-1, 'minvalue': 0},
        8: {'address':[16,18],'name': 'powerWgC', 'type': 'H', 'mtp': 1,'comment': 'C相无功功率','maxvalue': 256*256-1, 'minvalue': 0},
        9: {'address':[18,20],'name': 'energyZxyg', 'type': 'H', 'mtp': 0.1,'comment': '计算电量','maxvalue': 256*256-1, 'minvalue': 0},
        10: {'address':[20,22],'name': 'voltageA', 'type': 'H', 'mtp': 1,'comment': 'A相电压','maxvalue': 256*256-1, 'minvalue': 0},
        11: {'address':[22,24],'name': 'voltageB', 'type': 'H', 'mtp': 1,'comment': 'B相电压','maxvalue': 256*256-1, 'minvalue': 0},
        12: {'address':[24,26],'name': 'voltageC', 'type': 'H', 'mtp': 1,'comment': 'C相电压','maxvalue': 256*256-1, 'minvalue': 0},
        13: {'address':[26,28],'name': 'currentA', 'type': 'H', 'mtp': 1,'comment': 'A相电流','maxvalue': 256*256-1, 'minvalue': 0},
        14: {'address':[28,30],'name': 'currentB', 'type': 'H', 'mtp': 1,'comment': 'B相电流','maxvalue': 256*256-1, 'minvalue': 0},
        15: {'address':[30,32],'name': 'currentC', 'type': 'H', 'mtp': 1,'comment': 'C相电流','maxvalue': 256*256-1, 'minvalue': 0},
        16: {'address':[32,34],'name': 'frequencyA', 'type': 'H', 'mtp': 1,'comment': '频率','maxvalue': 256*256-1, 'minvalue': 0},
        17: {'address':[34,35],'name': 'powerFactorTotal', 'type': 'b', 'mtp': 1,'comment': '功率因素','maxvalue': 127, 'minvalue': 0},
    }

