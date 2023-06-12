#该项目已暂停更新
临近期末 因此不再更新该项目，如果想要实现定点抢课功能，可以提前登录到要选的课的页面，然后使用postman解析数据，半自动抢课，也能实现同样效果

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
3. 读取课程信息
4. 退课与选课操作
# 目前问题
问题：每个课程有一个密钥，并且竟然每次都不一样，只有请求对应的list返回的密钥才是当前密钥！
（等待重构代码中）

# 示例
![example](images/example.png)
