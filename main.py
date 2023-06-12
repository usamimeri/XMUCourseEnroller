import requests
from base64 import b64decode
from PIL import Image
import io
import time
import logging
from IPython.display import display
import json
logging.captureWarnings(True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

PASSWORD = ''  # 输入从官网中登录后，查看被md5和base64加密后的密码
ID = ''
TEACHINGCLASSTYPE = {
    '校选课': 'XGKC',
    '本专业计划课程': 'TJKC',
    '本专业其他年级课程': 'FANKC',
    '体育课程': 'TYKC',
}


def login_enroll(id, password_encryption):
    '''传入学号的加密后的密码，获得身份认证token'''
    session = requests.Session()
    captcha_url = 'http://xk.xmu.edu.cn/xsxkxmu/auth/captcha'
    try:
        logging.info('正在请求验证码')
        response = session.post(captcha_url)  # 不允许get方法
    except:
        raise '请求验证码失败'
    image_data = response.json()['data']['captcha'].split(',')[
        1]  # 获取base64原字符
    uuid = response.json()['data']['uuid']  # 参数验证
    b64_data = b64decode(image_data)  # 编码为base64
    image = Image.open(io.BytesIO(b64_data))
    display(image)  # 显示在单元格下方
    captcha = input('输入captcha的内容')
    data = {
        'loginname': id,
        'password': password_encryption,
        'captcha': captcha,
        'uuid': uuid
    }
    logging.info('正在尝试登录')
    login = session.post(
        'http://xk.xmu.edu.cn/xsxkxmu/auth/login', data=data, allow_redirects=False)
    try:
        token = login.json()['data']['token']  # 获取JWT身份认证
    except TypeError:
        logging.error('获取token失败，请检查你的学号的密码或验证码的正确性')
        raise '获取token失败'
    else:
        logging.info('成功获取token')
        return token


def query_course_list(token: str, classtypes:list):
    '''获取可选课程列表，可以选择哪种课程，返回课程目前人数，人数上限，
    教师 课程密钥 课程名称 课程classid 并存储到本地'''
    infos = {}
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json;charset=UTF-8',  # 必须加这个，不然会返回html
    }
    list_url = 'http://xk.xmu.edu.cn/xsxkxmu/elective/clazz/list'
    for classtype in classtypes:
        session = requests.Session()
        payload = "{"+f'\"teachingClassType\":\"{classtype}\",\"pageNumber\":1,\"pageSize\":10,\"orderBy\":\"\",\"campus\":\"1\"'+"}"
        courses = session.post(list_url, headers=headers, data=payload)

        page_num = (json.loads(courses.text)['data']['total']//10)+1 #比如五个课程只要遍历1页，15个课程遍历2页
        
        logging.info(f'获得课程类型:{classtype}共{page_num}页数')
        for pageNumber in range(1,page_num+1):  # 一旦满课程数返回空字典就break 这里只是一个上限
            payload = "{"+f'\"teachingClassType\":\"{classtype}\",\"pageNumber\":{pageNumber},\"pageSize\":10,\"orderBy\":\"\",\"campus\":\"1\"'+"}"
            courses = session.post(list_url, headers=headers, data=payload)
            if json.loads(courses.text)['code']==403:
                logging.error('我想你可能爬得太快了')
                raise '爬太快了'
            logging.info(courses.text)
            rows=json.loads(courses.text)['data']['rows'] 
            course_data = rows # 获取字典 一行中有多个课程
            logging.info(f'正在提取{classtype}的第{pageNumber}页信息')
            for course in course_data:
                try:
                    data = course['tcList'][0]
                except:
                    data=course #校选课没有tcList
                info = {
                    'SKJS': data['SKJS'],  # 课程教师
                    'JXBID': data['JXBID'],  # 课程id
                    'numberOfSelected': data['numberOfSelected'],  # 课程选中数
                    'classCapacity': data['classCapacity'],  # 课程容量
                    'secretVal': data['secretVal'],  # 课程密钥
                    'classtype':classtype,
                }
                infos[data['KCM']] = info
            time.sleep(0.5) #建议设置 不然会403（辅导员警告）
    try:
        with open('课程信息.json','wx') as f:
            f.write(json.dumps(infos,ensure_ascii=False,indent=2))
            logging.info('成功生成课程信息')
    except:
        with open('课程信息.json','w') as f:
            f.write(json.dumps(infos,ensure_ascii=False,indent=2))
            logging.info('成功覆盖课程信息')




token = login_enroll(ID, PASSWORD)
query_course_list(token,TEACHINGCLASSTYPE.values())
