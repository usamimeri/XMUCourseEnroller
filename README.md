<h1 align="center" style="text-align:center;">XMUCourseEnroller</h1>

🚩<span style="color:red;">请注意,请把握尺度,控制正常访问频率,不要滥用该程序</span>

# 厦门大学选课系统选课程序(尽可能ipynb上运行看结果)
> 需要注意的是,由于上传的密码会经过md5和base64加密，因此程序中的PASSWORD常量必须是在官网抓包login那个加密后的密码
![password](images/password.gif)

# 当前功能
1. 登录并获得token
2. 读取任意课程类型，任意页的所有课程的信息
> 注意这里只需要读取一次，可以先登录和读取所有课程信息，然后就可以进行任意次的退课和选课操作了，不需要重新初始化一遍

3. 退课与选课操作
4. 循环选课操作

# 待加功能
1. 多线程抢课（危）
2. 对单课程多教学班的适配
3. 志愿适配
4. gui可视化
5. 定时功能 比如每一段时间抓取课程信息观察各科老师受欢迎程度，以便及时避雷

# 示例
![example](images/show.gif)
