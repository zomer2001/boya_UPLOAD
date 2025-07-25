"""
高级加密标准（Advanced Encryption Standard），又称Rijndael加密法，是美国联邦政府采用的一种区块加密标准。
对加密快和密钥的字节数都有一定的要求，AES密钥长度的最少支持为128、192、256，加密块分组长度128位。需要知道密钥才能解密。
pip install pycryptodome
"""

from Crypto.Cipher import AES
import base64

# BS = len(AES_SECRET_KEY)
# BS = 16
#AES加密方式
class AES_ENCRYPT(object):
    # global BS
    # padding算法
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    unpad = lambda s: s[0:-ord(s[-1:])]

    def __init__(self,AES_SECRET_KEY,IV):
        self.key = AES_SECRET_KEY
        self.IV = IV
        self.mode = AES.MODE_CBC

    # 加密函数
    def encrypt(self,text):

        cryptor = AES.new(self.key.encode("utf8"), self.mode, self.IV.encode("utf8"))
        self.ciphertext = cryptor.encrypt(bytes(AES_ENCRYPT.pad(text), encoding="utf8"))
        # AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题，使用base64编码
        return base64.b64encode(self.ciphertext).decode("utf-8")

    # 解密函数
    def decrypt(self, text):
        decode = base64.b64decode(text)
        cryptor = AES.new(self.key.encode("utf8"), self.mode, self.IV.encode("utf8"))
        plain_text = cryptor.decrypt(decode)
        return AES_ENCRYPT.unpad(plain_text).decode("utf-8")
