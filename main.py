import requests
from base64 import b64decode
from PIL import Image
import io
import logging
from IPython.display import display
import json
logging.captureWarnings(True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

PASSWORD='' #输入从官网中登录后，查看被md5和base64加密后的密码
ID=''
TEACHINGCLASSTYPE={
    '校选课':'XGKC',
    '本专业计划课程':'TJKC',
    '本专业其他年级课程':'FANKC',
    '体育课程':'TYKC',
}


def login_enroll(id,password_encryption):
    '''传入学号的加密后的密码'''
    session=requests.Session()
    captcha_url='http://xk.xmu.edu.cn/xsxkxmu/auth/captcha'
    try:
        logging.info('正在请求验证码')
        response=session.post(captcha_url) #不允许get方法
    except:
        raise '请求验证码失败'
    image_data=response.json()['data']['captcha'].split(',')[1] #获取base64原字符
    uuid=response.json()['data']['uuid'] #参数验证
    b64_data = b64decode(image_data) #编码为base64
    image=Image.open(io.BytesIO(b64_data)) 
    display(image) #显示在单元格下方
    captcha=input('输入captcha的内容')
    data={
        'loginname':id,
        'password':password_encryption,
        'captcha':captcha,
        'uuid':uuid
    }
    try:
        logging.info('正在尝试登录')
        login=session.post('http://xk.xmu.edu.cn/xsxkxmu/auth/login',data=data,allow_redirects=False)
    except:
        raise '登录失败！'
    else:
        logging.info('成功获取身份验证Autorization')
        token=login.json()['data']['token'] #获取JWT身份认证
    return token


def query_course_list(token,pageNumber,teachingClassType):
    '''获取可选课程列表，可以选择哪一页，哪种课程，返回课程目前人数，人数上限，
    教师 课程密钥 课程名称 课程classid 返回一个字典'''
    session=requests.Session()
    list_url='http://xk.xmu.edu.cn/xsxkxmu/elective/clazz/list'
    payload = "{"+f'\"teachingClassType\":\"{teachingClassType}\",\"pageNumber\":{pageNumber},\"pageSize\":10,\"orderBy\":\"\",\"campus\":\"1\"'+"}"
    headers={
        'Authorization':token,
        'Content-Type':'application/json;charset=UTF-8', #必须加这个，不然会返回html
        }
    courses=session.post(list_url,headers=headers,data=payload)
    course_data=json.loads(courses.text)['data']['rows'] #获取字典 一行中有多个课程
    infos=[]
    for course in course_data:
        data=course['tcList'][0]
        info={
            '课程名':data['KCM'],
            '课程ID':data['JXBID'],
            '选中人数':data['numberOfSelected'],
            '课程容量':data['classCapacity'],
            '课程密钥':data['secretVal']
        }
        infos.append(info)
    return infos


token=login_enroll(ID,PASSWORD)
query_course_list(token,1,TEACHINGCLASSTYPE['本专业计划课程'])
