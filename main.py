import requests
from lxml import etree
from base64 import b64decode
from PIL import Image
import io
from IPython.display import display


class Header:
    def __init__(self, Cookie=None, referer='http://xk.xmu.edu.cn/xsxkxmu/profile/index.html',
                 user_agent='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36', accept_language='zh-CN,zh;q=0.9'):
        """存储 HTTP 请求头信息"""
        self.__header = {
            'user-agent': user_agent,
            'accept-language': accept_language,
            'referer': referer,
            'Cookie': Cookie,
            'Origin':'http://xk.xmu.edu.cn',
        }

    @property
    def header(self):
        '''返回header字典'''
        return self.__header
    
    def update(self, Cookie: str = None, referer: str = None, user_agent: str = None):
        '''更新请求头'''
        if isinstance(referer, str):
            self._header['referer'] = referer
        if isinstance(user_agent, str):
            self._header['user-agent'] = user_agent
        if Cookie:
            self._header['Cookie'] = Cookie

PASSWORD=''
ID=''
header=Header()
session=requests.Session()
response=session.post('http://xk.xmu.edu.cn/xsxkxmu/auth/captcha',headers=header.header) #不允许get方法
image_data=response.json()['data']['captcha'].split(',')[1] #获取base64原字符
uuid=response.json()['data']['uuid'] #参数验证
b64_data = b64decode(image_data) #编码为base64
image=Image.open(io.BytesIO(b64_data)) 
display(image) #显示在单元格下方
captcha=input('输入captcha的内容')
data={
    'loginname':ID,
    'password':PASSWORD,
    'captcha':captcha,
    'uuid':uuid
}
login=session.post('http://xk.xmu.edu.cn/xsxkxmu/auth/login',data=data)
print(f'状态码:{login.status_code}')
print(f'网页信息:{login.text}')
