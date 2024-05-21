# 创建应用实例
import sys

# from wxcloudrun import app



# #robot = werobot.WeRoBot()#app_id='wx20b1396d77813bab',token='AAQ9G7sEAAABAAAAAAAZHBKxAjsPDrr0/hdLZiAAAAAraAdzKm8i8JwFJ68cDOJBtIHsmv3F8e00LCv7f+tYvrdcIYN+n7bDX7DzL30SBV0F41HP29O6/zzd24/PPjeAmEt1eV+92opWZoTZaYXE4803U3e+7eFwGqdjQCxZ5L6SFxz0e5v1XDMlpLF5mQd/oW6tQ3lCcFxS')
 
# # @robot.text
# # def hello_world():
# #     return 'Hello World!'
# # robot.config['HOST'] = '0.0.0.0'
# # robot.config['PORT'] = 80
# # #if __name__ == '__main__':
# # robot.run()


# # 启动Flask Web服务
# if __name__ == '__main__':
#     app.run(host=sys.argv[1], port=sys.argv[2])

from flask import Flask, request, jsonify
import requests
import json

from werobot.replies import process_function_reply
from werobot.messages.messages import MessageMetaClass, UnknownMessage
from werobot.messages.events import EventMetaClass, UnknownEvent

import logging
logging.basicConfig(level=logging.DEBUG)

def process_message(message):
    """
    Process a message dict and return a Message Object
    :param message: Message dict returned by `parse_xml` function
    :return: Message Object
    """
    message["type"] = message.pop("MsgType").lower()
    if message["type"] == 'event':
        message["type"] = str(message.pop("Event")).lower() + '_event'
        message_type = EventMetaClass.TYPES.get(message["type"], UnknownEvent)
    else:
        message_type = MessageMetaClass.TYPES.get(
            message["type"], UnknownMessage
        )
    return message_type(message)

app = Flask(__name__)

def sendmess(appid, mess):
    try:
        response = requests.post(
            f'http://api.weixin.qq.com/cgi-bin/message/custom/send?from_appid={appid}',
            
            data=json.dumps(mess),
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        app.logger.debug('接口返回内容%s', response.text)
        return response.text
    except requests.RequestException as e:
        app.logger.debug('接口返回错误%s', e)
        return str(e)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_request():
    if request.method == 'POST':
        app.logger.debug('消息推送%s', request.json)
        
        # 从请求头中获取 'x-wx-from-appid' 字段的值，如果不存在则使用空字符串
        #app.logger.debug('%s',request.headers)
        appid = request.headers.get('X-Wx-Appid', '')#'wx20b1396d77813bab')

        # 从请求体中解构出 ToUserName, FromUserName, MsgType, Content, 和 CreateTime 字段
        data = request.json
        message = process_message(data)
        ToUserName = data.get('ToUserName', '')
        FromUserName = data.get('FromUserName', '')
        MsgType = data.get('MsgType', '')
        Content = data.get('Content', '')
        CreateTime = data.get('CreateTime', '')

        app.logger.debug('推送接收的账号%s %s', ToUserName, CreateTime)
        
        if MsgType == 'text':
            if Content == '回复文字':  # 小程序、公众号可用
                mess = {
                    'touser': FromUserName,
                    'msgtype': 'text',
                    'text': {
                        'content': '这是回复的消息'
                    }
                }
                try:
                    sendmess(appid, mess)
                except Exception as e:
                    app.logger.debug('%s',e)
            return """
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
    </xml>
    """.format(source=FromUserName, target=ToUserName, time=CreateTime, content=Content)   
            return process_function_reply('something',message)#'success'
        else:
            return 'success'
    else:
        return '仅支持 POST 请求'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)
