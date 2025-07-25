
import time
import requests
import json
import base64
import hashlib,urllib.parse


class Get_datas(object):
    apiSecret = "dajNi7JfK7A6C9Ky52h2w9Kg8ggttd5o"
    def get_str(self,params):
        change = self.ksort(params)
        encode_param = urllib.parse.urlencode(change)
        signString = urllib.parse.unquote_plus(encode_param)
        return signString

    def geturl_str(self,params):
        encode_param = urllib.parse.urlencode(params)
        url_str = urllib.parse.unquote_plus(encode_param)

        return url_str

    def sha256(self, message):
        return hashlib.sha256(message.encode()).hexdigest().lower()

    def base64(self, message):
        return base64.b64encode(message.encode()).decode('utf-8').lower()

    def md5(self, message):
        return hashlib.md5(message.encode()).hexdigest().lower()

    def get_sign(self,params):
        signString = self.get_str(params)
        signStr = signString + self.apiSecret
        sign = self.md5(self.base64(self.sha256(signStr)))
        return sign

    def ksort(self,d):
        # reverse则是用来指定排序是倒序还是顺序，reverse = true则是倒序，
        # reverse = false时则是顺序，默认时reverse = false。

        return [(k, d[k]) for k in sorted(d.keys(), reverse=False)]

    # 获取数据
    def get_data(self,params):

        sign = self.get_sign(params=params)

        params['sign'] = sign

        url_str = self.geturl_str(params=[(k, params[k]) for k in params.keys()])

        r = requests.get('http://192.168.0.2:8020/openapi/getdata?' + url_str)

        res_dictionary =r.json().get('data')

        return  res_dictionary


        # filename = r'D:\ProgramData\DATA_UPLOAD_SERVER\names.json'
        #
        # with open(filename, 'w', encoding='utf-8') as f:
        #     f.write(json.dumps(res_dictionary, ensure_ascii=False))

#
# if __name__ == '__main__':
#     timestam = int(time.time())
#     time_new = str(timestam)
#     params = {"apiKey": '1555312928870420483',
#               "timestamp": time_new}
#     obj = Get_datas()
#     obj.get_data(params)


