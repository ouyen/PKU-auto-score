# PKU自动查成绩

用selenium随便写的小工具, 每30min自动查个成绩 , 之后用requests.get()调用自定义接口实现通知

使用方法:

1.使用云函数,tg等工具自行搭建一个通知链接,如 http://xxxxxx%s ,此工具会

```python
requests.get((http://xxxxxx%s)%message)
```
发送消息

2.按照`config copy.json`写`config.json`,时间的单位为分钟

```
{
    "username":"", 用户名
    "password":"", 密码
    "send_message_url":"", (1)中的url
    "sleep_time": 30 刷新时间,默认为30min
}
```

3.`pip -r requirements.txt`安装依赖
