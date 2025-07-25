

import requests
import logging
from datetime import datetime

def Reminder():
    # 时间
    now_time = datetime.now().date()

    SCKEY_list = ["SCT208727TiYJ0GuIrjYFvuH6heGWtGZvu"]

    content = f'##哈喽，早上好!今天是{now_time}。今天数据上传失败，请检测电脑网络情况~'

    payload = {"text": "建筑掉线提醒", "desp": content}

    print(payload)

    for SCKEY in SCKEY_list:
        print(SCKEY)
        url = f"https://sc.ftqq.com/{SCKEY}.send"

        response = requests.post(url,params=payload)

        logging.basicConfig(filename='log.log', format='%(asctime)s:%(message)s', level=logging.INFO)

        print(response.text)

        if response.json()['data']['error'] == 'SUCCESS':
            logging.info('发送成功')
        else:
            logging.warning('发送失败 %s' %response.json())

if __name__ =='__main__':
    Reminder()

