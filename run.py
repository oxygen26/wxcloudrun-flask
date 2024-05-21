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

# # insertion =======================================================
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.chat_engine import ContextChatEngine
import sys,os
#sys.path.append('/home/oxygen26/llama/python/')
#from core import llm_y
# * settings ==========================================================
from llama_index.core import Settings

from langchain.llms import QianfanLLMEndpoint
from llama_index.llms.langchain.base import LangChainLLM
#from llama_index.llms.openai import OpenAI

#llm_openai = OpenAI(api_key="sk-6zm8Aqt9A31MPRiDV7WJ17EhfsMNjwwApt8PLkmuLZCH8kdo",api_base="https://api.openai-proxy.org/v1",model='gpt-4')

"""For basic init and call"""

# 'Yi-34B-Chat','ERNIE-Bot-4','ERNIE-Speed-128k','ERNIE-Bot-turbo'
os.environ["QIANFAN_AK"] = "2kFfoTXEOjItYtBAQtVZUv17" #"Q0gXTGHI4oM17zMbI3sMeqIg"#
os.environ["QIANFAN_SK"] = "s38GyXy4v8xipic8rIlVkm0gTeBL4zkU" #"iWmqKV7A1WSVwatdbmOxK4L5Av1Goxqf"#

qllm_y = QianfanLLMEndpoint(model='Yi-34B-Chat',#'Yi-34B-Chat','ERNIE-Bot-4','ERNIE-Speed-128k','ERNIE-Bot-turbo'
                           #streaming=True,
                        ak=os.getenv('QIANFAN_AK'), sk=os.getenv('QIANFAN_SK'),**{'top_p': 0.8, 'temperature': 0.1, 'penalty_score': 1})
#res = llm("hi")
qllm_wx = QianfanLLMEndpoint(model='ERNIE-Speed-128k',#'Yi-34B-Chat','ERNIE-Bot-4','ERNIE-Speed-128k','ERNIE-Bot-turbo'
                           #streaming=True,
                        ak=os.getenv('QIANFAN_AK'), sk=os.getenv('QIANFAN_SK'),**{'top_p': 0.8, 'temperature': 0.1, 'penalty_score': 1})
qllm_wx4 = QianfanLLMEndpoint(model='ERNIE-4.0-8K',#'Yi-34B-Chat','ERNIE-Bot-4','ERNIE-Speed-128k','ERNIE-Bot-turbo'
                           #streaming=True,
                        ak=os.getenv('QIANFAN_AK'), sk=os.getenv('QIANFAN_SK'),**{'top_p': 0.8, 'temperature': 0.1, 'penalty_score': 1})
#-----------------------------------------------------
llm_y = LangChainLLM(llm=qllm_y)
Settings.llm = llm_y

# messages = [
#     ChatMessage(
#         #role="system", content="You are a pirate with a colorful personality"
#     ),
#     ChatMessage(role="user", content="hi"),
# ]

#custom_chat_history = [ChatMessage(role= (MessageRole.USER if i['role']=='user' else MessageRole.ASSISTANT),content=i['content']) for i in session.messages]
#for wenxin_model in ['Yi-34B-Chat','ERNIE-Bot-4','ERNIE-Speed-128k','ERNIE-Bot-turbo']:
llama_flag=0
try:
                    
    from llama_index.core.retrievers import QueryFusionRetriever
    retriever = QueryFusionRetriever(
        [commit_sctx.std_retriever(), commit_file_sctx.std_retriever()],
        similarity_top_k=2,
        num_queries=1,  # set this to 1 to disable query generation
        use_async=False,#True,
        verbose=True,
        # query_gen_prompt="...",  # we could override the query generation prompt here
    )
    # query_engine = RetrieverQueryEngine(node_postprocessors=[MetadataReplacementPostProcessor(target_metadata_key="window")],
    #             retriever=retriever,
    #             response_synthesizer=synth
    #             )#.query('生物信息学，给出参考链接')
    chat_engine = ContextChatEngine.from_defaults(
        retriever=retriever,#commit_sctx.query_engine(),
    #condense_question_prompt=custom_prompt,
        #chat_history=custom_chat_history[:-1],
        #service_context=service_context,
        verbose=True
    )
    #break
except Exception as e:
    print('query engine error::',e)
    #break
    try:
        from llama_index.core.chat_engine import SimpleChatEngine

        chat_engine = SimpleChatEngine.from_defaults(
            #chat_history=custom_chat_history[:-1],
        #service_context=service_context,
        verbose=False)
    except Exception as e:
        print('simple engine error::',e)

def chat(messages):
    response_text = {'result':chat_engine.chat(
            messages#custom_chat_history[-1].content
            ).response,"usage":{"total_tokens":2,"completion_tokens":1}}
    return response_text['result']
    #llama_flag=1
        #break
        #insertion =------------===========================================

@app.route('/wechat', methods=['POST'])
def wechat():
    # 检查 Content-Type 是否为 application/json
    app.logger.debug(request.content_type)
    if request.content_type == 'application/json':
        try:
            # 解析 JSON 数据
            json_data = request.json
            app.logger.debug('接收到的 JSON 数据:%s', json_data)

            # 将 JSON 数据转换为 XML
            xml_data = json_to_xml(json_data)
        except Exception as e:
            app.logger.debug('解析 JSON 数据失败:%s', e)
            xml_data = request.data
    elif request.content_type == 'application/xml':
        xml_data = request.data
    else:
        return 'Content-Type 不支持', 400
    app.logger.debug('转换后的 XML 数据:%s', xml_data.decode('utf-8'))

    # 处理 XML 数据并生成响应
    response_data = handle_xml_data(xml_data)
    app.logger.debug('生成的响应数据:%s', response_data)
    response = make_response(response_data)
    response.content_type = 'application/xml'
    return response
    
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
    xml = ET.fromstring(xml_data)

    try:
        to_user = xml.find('ToUserName').text
    except:
        to_user=''
    try:
        from_user = xml.find('FromUserName').text
    except:
        from_user=''
    try:
        msg_type = xml.find('MsgType').text
    except:
        msg_type=''
    try:
        content = xml.find('Content').text if msg_type == 'text' else ''
    except:
        content=''
    app.logger.debug(f'ToUserName: {to_user}')
    app.logger.debug(f'FromUserName: {from_user}')
    app.logger.debug(f'MsgType: {msg_type}')
    app.logger.debug(f'Content: {content}')

    if content == '回复文字' :
        reply_content = '这是回复的消息' 
    
    else:
        reply_content=chat(content) #f'收到你的消息：{content}'
    response_xml = generate_reply(from_user, to_user, reply_content)
    
    return response_xml

def generate_reply(to_user, from_user, content):
    reply_xml = TextReply.TEMPLATE.format(target=to_user, source=from_user, time=int(time.time()), content=content)
    return reply_xml

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)
