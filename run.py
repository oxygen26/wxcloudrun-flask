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
from werobot.replies import * #process_function_reply
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
    TextReply.TEMPLATE.format(to_user, from_user, int(time.time()), content)
    return reply_xml

def json_to_xml(json_data):
    # 创建 XML 根元素
    root = ET.Element("xml")
    
    # 递归转换 JSON 数据为 XML 元素
    def build_xml_element(parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(parent, key)
                build_xml_element(child, value)
        elif isinstance(data, list):
            for item in data:
                child = ET.SubElement(parent, "item")
                build_xml_element(child, item)
        else:
            parent.text = str(data)

    build_xml_element(root, json_data)
    
    # 生成 XML 字符串
    xml_str = ET.tostring(root, encoding='utf-8')
    return xml_str
@app.route('/wechat', methods=['POST'])
def wechat():
    # 检查 Content-Type 是否为 application/json
    if request.content_type == 'application/json':
        try:
            # 解析 JSON 数据
            json_data = request.json
            app.logger.debug('接收到的 JSON 数据:%s', json_data)

            # 将 JSON 数据转换为 XML
            xml_data = json_to_xml(json_data)
            app.logger.debug('转换后的 XML 数据:%s', xml_data.decode('utf-8'))

            # 处理 XML 数据并生成响应
            response_data = handle_xml_data(xml_data)
            app.logger.debug('生成的响应数据:%s', response_data.decode('utf-8'))
            response = make_response(response_data)
            response.content_type = 'application/xml'
            return response
        except Exception as e :
            app.logger.debug('处理 XML 数据出错:%s', e)#json.JSONDecodeError as e:
            return f'JSON 解析错误: {e}', 400
    else:
        return 'Content-Type 必须为 application/json', 400

def json_to_xml(json_data):
    # 创建 XML 根元素
    root = ET.Element("xml")
    
    # 递归转换 JSON 数据为 XML 元素
    def build_xml_element(parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(parent, key)
                build_xml_element(child, value)
        elif isinstance(data, list):
            for item in data:
                child = ET.SubElement(parent, "item")
                build_xml_element(child, item)
        else:
            parent.text = str(data)

    build_xml_element(root, json_data)
    
    # 生成 XML 字符串
    xml_str = ET.tostring(root, encoding='utf-8')
    return xml_str

def handle_xml_data(xml_data):
    # 解析 XML 数据并生成响应
    try:
        xml = ET.fromstring(xml_data)

        to_user = xml.find('ToUserName').text
        from_user = xml.find('FromUserName').text
        msg_type = xml.find('MsgType').text
        content = xml.find('Content').text if msg_type == 'text' else ''

        app.logger.debug(f'ToUserName: {to_user}')
        app.logger.debug(f'FromUserName: {from_user}')
        app.logger.debug(f'MsgType: {msg_type}')
        app.logger.debug(f'Content: {content}')

        reply_content = '这是回复的消息' if content == '回复文字' else f'收到你的消息：{content}'
        response_xml = generate_reply(from_user, to_user, reply_content)
        
        return response_xml
    except Exception as e:
        app.logger.debug('错误! %s',e)
        return f'XML 解析错误: {e}', 400

def generate_reply(to_user, from_user, content):
    reply_xml = f"""
    <xml>
      <ToUserName><![CDATA[{to_user}]]></ToUserName>
      <FromUserName><![CDATA[{from_user}]]></FromUserName>
      <CreateTime>{int(time.time())}</CreateTime>
      <MsgType><![CDATA[text]]></MsgType>
      <Content><![CDATA[{content}]]></Content>
    </xml>
    """
    return reply_xml

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)
