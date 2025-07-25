
"""
观察者模式进行信息订阅
"""
from tools.logging_conf import logger
from tools.webservice_client import Webservice_Server

class NewsPublisher:
    def __init__(self):
        self.__subscribers = []
        # self.__latestNews =None
        self.__latestNews = {}

    def attach(self,subscriber):
        self.__subscribers.append(subscriber)

    def detach(self):
        return self.__subscribers.pop()

    #生成观察者列表
    def subscribers(self):
        return [type(x).__name__ for x in self.__subscribers]

    def notifySubscribers(self):
        for sub in self.__subscribers:
            sub.update()

    # def addNews(self,news):
    #     # self.__latestNews = news

    def addNews(self,K,V):
        self.__latestNews[K] = V

    def getNews(self):
        #print(("Got News:",self.__latestNews))
        return self.__latestNews

from abc import ABCMeta,abstractmethod
class Subscriber(metaclass=ABCMeta):
    @abstractmethod
    def update(self):
        pass


#webservice接口订阅服务
class Webservice_Subscriber(Subscriber):

    def __init__(self, publisher):

        self.publisher = publisher
        self.publisher.attach(self)

    def update(self):
        xml_str=self.publisher.getNews()
        print('getnews sunccess')

        s = buildingId='440300' + list(xml_str.keys())[0]
        print(s)
        s = '440300C125'
        try:
            # 调用服务
            obj = Webservice_Server(s)
        except Exception as e:
            print(f"发生错误: {e}")
        print('初始化成功')
        obj.get_model(data=list(xml_str.values())[0])

        logger.info("数据上传成功")


