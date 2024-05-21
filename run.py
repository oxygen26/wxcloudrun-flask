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

import requests
import json,time

from flask import Flask, request, make_response

import hashlib
import xml.etree.ElementTree as ET
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

def check_signature(token, signature, timestamp, nonce):
    # 按照微信公众平台的要求进行签名验证
    lst = [token, timestamp, nonce]
    lst.sort()
    sha1 = hashlib.sha1()
    sha1.update("".join(lst).encode('utf-8'))
    hashcode = sha1.hexdigest()
    return hashcode == signature

def generate_reply(to_user, from_user, content):
    # 生成回复消息的 XML 格式
    reply_xml = """
    <xml>
      <ToUserName><![CDATA[{0}]]></ToUserName>
      <FromUserName><![CDATA[{1}]]></FromUserName>
      <CreateTime>{2}</CreateTime>
      <MsgType><![CDATA[text]]></MsgType>
      <Content><![CDATA[{3}]]></Content>
    </xml>
    """.format(to_user, from_user, int(time.time()), content)
    return reply_xml

@app.route('/wechat', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_request():
    if request.method == 'POST':
        # app.logger.debug('消息推送:%s', request.json)
        
        # # 从请求头中获取 'x-wx-from-appid' 字段的值，如果不存在则使用空字符串
        # #app.logger.debug('请求头%s',request.headers)
        # appid = request.headers.get('X-Wx-Appid', '')#'wx20b1396d77813bab')
        # app.logger.debug('appid:%s',appid)

        # # 从请求体中解构出 ToUserName, FromUserName, MsgType, Content, 和 CreateTime 字段
        # data = request.json
        # #message = process_message(data)
        # ToUserName = data.get('ToUserName', '')
        # FromUserName = data.get('FromUserName', '')
        # MsgType = data.get('MsgType', '')
        # Content = data.get('Content', '')
        # CreateTime = data.get('CreateTime', '')

        # app.logger.debug('推送接收的账号:%s %s', ToUserName, CreateTime)
        
        json_str = request.data
        app.logger.debug('Received POST request with data: %s', json_str)
        
        import xml.etree.ElementTree as ET
        try:
            xmls = ET.fromstring(json_str)
        except Exception as e:
            #import xml
            import json
            data = json.loads(json_str)

            # 创建 XML 元素
            root = ET.Element("xml")

            for key, value in data.items():
                element = ET.SubElement(root, key)
                element.text = str(value)

            # 生成 XML 字符串
            xml_str = ET.tostring(root, encoding='utf-8')
            xmls = ET.fromstring(xml_str)
            app.logger.debug('Received POST request with xml_str: %s', xml_str)

    
        ToUserName = xmls.find('ToUserName').text if xmls.find('ToUserName') else ''
        FromUserName = xmls.find('FromUserName').text if xmls.find('FromUserName') else ''
        MsgType = xmls.find('MsgType').text if xmls.find('MsgType') else  ''
        Content = xmls.find('Content').text if MsgType == 'text' else ''

        app.logger.debug('Parsed XML - ToUserName: %s, FromUserName: %s, MsgType: %s, Content: %s', ToUserName, FromUserName, MsgType, Content)
        
        
        if 1:#MsgType == 'text':
            if Content == '回复文字':
                reply_content = '这是回复的消息'
            else:
                reply_content = '收到你的消息：' + Content
        else:
            reply_content = '暂不支持此类型消息'

        response_xml = generate_reply(FromUserName, ToUserName, reply_content)
        app.logger.debug('回复消息：%s', response_xml)
        response = make_response(response_xml)
        
        response.content_type = 'application/xml'
        #app.logger.debug('response对象%s',response.json())
        return response


    elif 0:#request.method == 'POST':
        app.logger.debug('消息推送%s', request.json)
        
        # 从请求头中获取 'x-wx-from-appid' 字段的值，如果不存在则使用空字符串
        #app.logger.debug('请求头%s',request.headers)
        appid = request.headers.get('X-Wx-Appid', '')#'wx20b1396d77813bab')
        app.logger.debug('appid%s',appid)

        # 从请求体中解构出 ToUserName, FromUserName, MsgType, Content, 和 CreateTime 字段
        data = request.json
        message = process_message(data)
        ToUserName = data.get('ToUserName', '')
        FromUserName = data.get('FromUserName', '')
        MsgType = data.get('MsgType', '')
        Content = data.get('Content', '')
        CreateTime = data.get('CreateTime', '')

        app.logger.debug('推送接收的账号%s %s', ToUserName, CreateTime)
        
        if 1 :#MsgType == 'text':
            if 1:#Content == '回复文字':  # 小程序、公众号可用
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
                    app.logger.debug('发送错误%s',e)
    #         return """
    # <xml>
    # <ToUserName><![CDATA[{target}]]></ToUserName>
    # <FromUserName><![CDATA[{source}]]></FromUserName>
    # <CreateTime>{time}</CreateTime>
    # <MsgType><![CDATA[text]]></MsgType>
    # <Content><![CDATA[{content}]]></Content>
    # </xml>
    # """.format(source=FromUserName, target=ToUserName, time=CreateTime, content=Content)   
            return process_function_reply('something',message)#'success'
        else:
            return 'success'
    else:
        return '仅支持 POST 请求'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)
