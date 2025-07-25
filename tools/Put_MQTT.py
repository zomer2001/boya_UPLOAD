
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
rootPath = os.path.split(BASE_DIR)[0]
sys.path.append(rootPath)

from paho.mqtt import client as mqtt
import time
# from tools.config_file import config
#发布服务
class Pub_Server(object):
    def __init__(self):
        # self.MQTTHOST = config.get('mqtthost')  # MQTT服务器地址
        # self.MQTTPORT = int(config.get('mqttport'))  # MQTT端口  1883
        self.MQTTHOST = "139.159.236.24"  # MQTT服务器地址
        self.MQTTPORT = 1883  # MQTT端口  1883
        self.client_id = 'Q002'  # client代表设备uuid
        self.mqttClient = mqtt.Client(self.client_id)

    def on_connect(self,client, userdata, flags, rc):
        """一旦连接成功, 回调此方法"""
        rc_status = ["连接成功", "协议版本错误", "无效的客户端标识", "服务器无法使用", "用户名或密码错误", "无授权"]
        global connect_alive

        if rc == 0:
            connect_alive = True
            print("控制器{}连接服务器{}:{}成功".format(self.client_id, self.MQTTHOST, self.MQTTPORT,
                                                                         rc_status[rc]))
        else:
            connect_alive = False
            print("控制器{}连接服务器{}:{}失败：{}，10秒后再次连接".format(self.client_id,self.MQTTHOST,self.MQTTPORT, rc_status[rc]))
            time.sleep(10)
            self.mqtt_connect()
            self.mqttClient.subscribe(self.topic)

    def on_connect_fail(self,client, userdata):
        """连接失败触发"""
        global connect_alive
        print("控制器{}连接服务器{}:{}失败：通讯异常，10秒后再次连接".format(self.client_id, self.MQTTHOST, self.MQTTPORT))
        connect_alive = False
        time.sleep(10)
        self.mqtt_connect()
        self.mqttClient.subscribe(self.topic)

    def on_disconnect(self,client, userdata, rc):
        """连接中断触发"""
        global connect_alive
        print("控制器{}连接服务器{}:{}连接中断，10秒后再次连接".format(self.client_id, self.MQTTHOST, self.MQTTPORT))
        connect_alive = False
        time.sleep(10)
        self.mqtt_connect()
        self.mqttClient.subscribe(self.topic)

    def mqtt_connect(self):
        """连接MQTT服务器"""
        self.mqttClient.on_connect = self.on_connect  # 返回连接状态的回调函数

        self.mqttClient.on_connect_fail = self.on_connect_fail
        self.mqttClient.on_disconnect = self.on_disconnect

        # self.mqttClient.username_pw_set("pedf", "pedf0308")  # mqtt服务器账号密码
        self.mqttClient.connect(self.MQTTHOST,self.MQTTPORT,keepalive=60)

        self.mqttClient.loop_start()  # 启用线程连接
        return self.mqttClient

    # 发布消息
    def mqtt_publish(self,topic,msg_pub):
        """发布主题为'A002/PUB',内容为'msg_pub',服务质量为2"""
        mqttClient = self.mqtt_connect()
        # msg=f"{msg_pub}"
        msg = msg_pub
        mqttClient.publish(topic,msg,qos=0)
        mqttClient.loop_stop()

if __name__ == '__main__':
    topic = "U001/PUB"
    hex_bytes= b"\x05\x0d\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x91\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff\xff\x38"

    msg_pub = hex_bytes
    # print(hex_bytes.hex())
    print(msg_pub)
    Pub_object = Pub_Server()
    Pub_object.mqtt_publish(topic,msg_pub)
