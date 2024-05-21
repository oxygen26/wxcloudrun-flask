from werobot import WeRoBot
from werobot.replies import WeChatReply, TextReply, ImageReply, MusicReply,ArticlesReply, Article
import re
import urllib
import logging
import json
from flask import Flask
import requests
robot = WeRoBot(
    #token='xxxxxx',# 对应公众号的token设置
    #encoding_aes_key='xxxxxx',# 明文传输不需要填写
    app_id='wx20b1396d77813bab'#明文传输不需要填写
)

import random
# 明文模式不需要下面三项
#robot.config["APP_ID"]=''
#robot.config["APP_SECRET"]=''
#robot.config['ENCODING_AES_KEY'] = ''


timeout=30                                                       # 超时时间
bdkey = 'xxxxxxx'      # 百度天气ak
def get_citys_in_msg(msg):
    # 获取消息中包含的城市
    api_url = 'http://www.yangyingming.com/api/parse_city?%s'%(urllib.parse.urlencode({'msg':msg}))
    citys = urllib.request.urlopen(api_url).read().decode('utf8')
    return citys

def get_weather(city):
    # 获取天气数据
    url = 'http://wthrcdn.etouch.cn/weather_mini'
    param = urllib.parse.urlencode({
        'city':city,
    })
    api_url = '%s?%s'%(url,param)
    wdata = requests.get(api_url).text
    return wdata

# 被关注
@robot.subscribe
def subscribe(message):
    return '你好~\n我是xxxx的管家机器人，我叫xxxx T_T\n有什么能帮您的吗？/::$'
@robot.handler
def echo(message):
    try:
        msg = message.content
        if re.compile(".*?天气.*?").match(msg):
            res_msg = ''
            # 取出该消息中包含的所有城市
            citys = get_citys_in_msg(msg).split(',')
            # 获得每一座城市的天气状况
            if citys[0]=='':
                return '亲爱的，你想知道哪座城市的天气呢？'
            else:
                for city in citys:
                    if res_msg!='':
                        res_msg += '\n\n'
                    wdata = get_weather(city)
                    wdata = json.loads(wdata)
                    if wdata['desc']=='OK':
                        wdata=wdata['data']
                        res_msg += '当前位置：%s\n温馨提示: %s\n当前温度: %s+℃\n昨天: %s\n风力:%s \n风向: %s\n%s,%s\n天气: %s\n ----------------------------' % (
                        wdata['city'], wdata['ganmao'], wdata['wendu'], wdata['yesterday']['date'], wdata['yesterday']['fl'][9:[m.start() for m in re.finditer(']', wdata['yesterday']['fl'])][0]], wdata['yesterday']['fx'], wdata['yesterday']['high'], wdata['yesterday']['low'], wdata['yesterday']['type'])
                        for i in range(4):
                            res_msg += '\n时间: %s\n风力：%s\n风向：%s\n%s,%s\n天气: %s \n ----------------------------' % (wdata["forecast"][i]['date'], wdata["forecast"][i]['fengli'][9:[m.start() for m in re.finditer(
                            ']', wdata['yesterday']['fl'])][0]], wdata["forecast"][i]['fengxiang'], wdata["forecast"][i]['high'], wdata["forecast"][i]['low'], wdata["forecast"][i]['type'])
                    else:
                        res_msg += '没有找到%s的天气信息'%city
                return res_msg
        else:
            # 提取消息
            msg = message.content.strip().lower()
            # 解析消息
            if  re.compile(".*?你好.*?").match(msg) or\
                re.compile(".*?嗨.*?").match(msg) or\
                re.compile(".*?哈喽.*?").match(msg) or\
                re.compile(".*?hello.*?").match(msg) or\
                re.compile(".*?hi.*?").match(msg) or\
                re.compile(".*?who are you.*?").match(msg) or\
                re.compile(".*?你是谁.*?").match(msg) or\
                re.compile(".*?你的名字.*?").match(msg) or\
                re.compile(".*?什么名字.*?").match(msg) :
                return "xxxxxxx，我叫xxxxx T_T\n有什么能帮您的吗？/::$"
            elif re.compile(".*?厉害.*?").match(msg):
                return '承让承让 /:B-)/:B-)/:B-)'
            elif re.compile(".*?想你.*?" ).match(msg):
                return '我也想你'
            elif re.compile(".*?miss you.*?").match(msg):
                return 'I miss you,too /::$/::$ /::$/::$'
            elif re.compile(".*?我爱你.*?").match(msg):
                return '我也爱你 /:showlove/:showlove/:showlove/:showlove'
            elif re.compile(".*?love you.*?").match(msg):
                return 'I love you,too'
            elif re.compile(".*?美女.*?").match(msg):
                return '我是男生哦♂/:rose/:rose/:rose'
            elif re.compile(".*?帅哥.*?").match(msg):
                return '谢谢夸奖 /:rose/:rose/:rose/:rose'
            elif re.compile(".*?傻逼.*?").match(msg):
                return '爸爸不想理你/:pig/:pig/:pig'
            else:
                return msg
    except Exception as e:
        print (e)

# 读取文档里的笑话，把前三行存在 data2 里，字符串太长公众号会报错
def joke_data():
    filename = 'qiushibaike.txt'
    f = open(filename, 'r')
    data = f.readline()
    f.close()
    # data1 = data.split()
    # data2 = ''
    # for data_i in data1[0:3]:
    #     data2 += data_i + '\n' + '\n'
    return data

# 读取文档里的电影名称
def movie_name():
    filename = 'movies_name.txt'
    f = open(filename, 'r')
    data = f.read()
    f.close()
    return data

# 从三首音乐里随机选一首
def music_data():
    music_list = [
            ['童话镇','陈一发儿','https://e.coka.la/wlae62.mp3','https://e.coka.la/wlae62.mp3'],
            ['都选C','缝纫机乐队','https://files.catbox.moe/duefwe.mp3','https://files.catbox.moe/duefwe.mp3'],
            ['精彩才刚刚开始','易烊千玺','https://e.coka.la/PdqQMY.mp3','https://e.coka.la/PdqQMY.mp3']
            ]
    num = random.randint(0,2)
    return music_list[num]

# 读取 fight.txt 里的句子，随机返回一句
def get_fighttxt():
    filename = 'fight.txt'
    f = open(filename, 'r')
    data = f.read()
    f.close()
    data1 = data.split()
    max_num = len(data1) - 1
    num = random.randint(0, max_num)
    data2 = data1[num]
    return data2

# 匹配 笑话 回复糗百笑话
@robot.filter('笑话')
def joke(message):
    data = joke_data()
    return data

@robot.filter('xxxxx')
def joke(message):
    msg='xxxxx'
    return msg
#如果用
#@robot.text
#def joke(message):
#    if message.content == "笑话":
#会报错
#UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal

# 匹配 电影 回复电影名称
@robot.filter('电影')
def movie(message):
    name = movie_name()
    return name

# blog 回复个人博客
@robot.filter('blog')
def blog(message):
    reply = ArticlesReply(message=message)
    article = Article(
        title="xxxxx",
        description="xxxx",
        img="xxxxxx",
        url="xxxxx"
    )
    reply.add_article(article)
    return reply

# 匹配 音乐 回复一首歌
@robot.filter('音乐')
def music(message):
    music1 = music_data()
    return music1

# 匹配 fight 回复一句话
@robot.filter('fight')
def fight(message):
    data = get_fighttxt()
    return data


