# XMUCourseEnroller
厦门大学选课系统抢课程序
# 主要思路
1. 向captcha网址发送post，将返回的base64编码的验证码图片在本地显示
2. 向login的链接发送登录请求，获得JWT验证token
3. 将token加入后续的请求头中
4. （可选）向list发送请求，获得所有课程的密钥、classid、选中人数、课程上限、课程名、课程老师（这里需要解析json），这里需要把preload加入data
5. 向add或del的url发送post请求即可实现选课， 注意需要包装一个preload传入课程
# 当前功能
1. 登录并获得token
2. 读取任意课程类型，任意页的所有课程的信息

# 示例
![EX8]%ZS@DELX0UZ~D_E2EDG.png](EX8]%ZS@DELX0UZ~D_E2EDG.png)
