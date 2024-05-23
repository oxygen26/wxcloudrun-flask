import werobot
import requests

robot = werobot.WeRoBot(token='alphabeta'#,encoding_aes_key = 'sQWIMyo4AzgjmUczG99Uh3Cirj7XB2UeYTpKYpJE3TB',app_id = 'wx20b1396d77813bab'
)

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
llm_wx = LangChainLLM(llm=qllm_wx)
llm_wx4 = LangChainLLM(llm=qllm_wx4)
Settings.llm = llm_wx#y

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
    while True:
        try:
            response_text = chat_engine.chat(
            messages#custom_chat_history[-1].content
        )
            return response_text#['result']
        except Exception as e:
            print('chat errorxxxxxxxxxxxxxxxx',e)
            time.sleep(1)
            pass    
    #llama_flag=1
        #break
        #insertion =------------===========================================

@robot.text#handler
def hello_world(content):
    a = chat(content.content).response
    print('=========================',a)
    #print(type(a))
    return a#'Hello World!'

from flask import Flask,request
import time
import xml.etree.cElementTree as ET
from werobot.contrib.flask import make_view
from WXBizMsgCrypt3 import WXBizMsgCrypt

app=Flask(__name__)
app.add_url_rule(rule='/robot/', # WeRoBot 的绑定地址
                endpoint='werobot', # Flask 的 endpoint
                view_func=make_view(robot),
                methods=['GET', 'POST'])

sToken = 'alphabeta'  # 对应上图的Token
sEncodingAESKey = 'sQWIMyo4AzgjmUczG99Uh3Cirj7XB2UeYTpKYpJE3TB'  # 对应上图的EncodingAESKey
sReceiveId = 'wwba862ea99070d024'  # 对应企业ID，即corpid
wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sReceiveId)

def get_access_token():
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    params = {
        'corpid': 'wwba862ea99070d024',
        'corpsecret': '48QnzNZWxD6VwW2-r6LyYaEKWyotKs8vFDmF_bP0tkM' }
    response = requests.get(url, params=params)
    access_token = response.json().get('access_token')
    return access_token

def get_message(access_token, token,open_kfid):
    url = f'https://qyapi.weixin.qq.com/cgi-bin/kf/sync_msg?access_token={access_token}'
    data={
    "cursor": "",
    "token": token,
    "limit": 1000,
    "voice_format": 0,
    "open_kfid": open_kfid}
    response = requests.post(url, json=data)
    return response.json()

def send_message(access_token, open_kfid,external_userid,msg_id,content):
    url = f'https://qyapi.weixin.qq.com/cgi-bin/kf/send_msg?access_token={access_token}'
    data={
   "touser" : external_userid,
   "open_kfid": open_kfid,
   "msgid": msg_id,
   "msgtype" : "text",
   "text" : {
       "content" :content
   }
}
    response = requests.post(url, json=data)
    return response.json()

@app.route('/robot1/', methods=['GET', 'POST'])
def robot():
    msg_signature = request.args.get('msg_signature')  # 企业微信加密签名
    timestamp = request.args.get('timestamp')  # 时间戳
    nonce = request.args.get('nonce')  # 随机数
    echostr = request.args.get('echostr')  # 加密字符串

    # 验证URL有效性
    if request.method == 'GET':
        ret, sReplyEchoStr = wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
        if ret == 0:
            return sReplyEchoStr
        else:
            return 'ERR: VerifyURL ret:' + str(ret)

    # 接收消息
    if request.method == 'POST':
        try:
            print(request.json)
        except Exception as e:
            print('json????????????????????????',e)
        print("请求消息:\n",request.data)
        ret, xml_content = wxcpt.DecryptMsg(request.data, msg_signature, timestamp, nonce)
        if ret == 0:
            root = ET.fromstring(xml_content)
            print('解密消息\n',xml_content)
            
            msg_type = root.find('MsgType').text
            if msg_type == 'event':
                event = root.find('Event').text
                if event =='kf_msg_or_event':
                    token = root.find('Token').text
                    open_kfid = root.find('OpenKfId').text
                    access_token  = get_access_token()
                    print('access_token--------------\n',access_token, token,open_kfid)
                    message = get_message(access_token, token,open_kfid)
                    #print('message-----------------\n',message)
                    message1 = message.get('msg_list')[-1]
                    msg_id =message1.get('msgid')
                    external_userid = message1.get('external_userid')
                    content = message1.get('text').get('content')
                    print('content-----------------\n',msg_id,' ',content)
                    return_message = chat(content).response
                    print('return_message-------------------\n',return_message)
                    send_j = send_message(access_token, open_kfid, external_userid,msg_id,return_message)
                    print('send_message:====================',send_j)
                    return 'success'
                elif event == 'subscribe':
                    return '欢迎关注'
                else:
                    return 'success'
            elif msg_type =='text':
                to_user_name = root.find('ToUserName').text
                try:
                    from_user_name = root.find('FromUserName').text
                except:
                    from_user_name = ''
                create_time = root.find('CreateTime').text
                
                content = root.find('Content').text
                msg_id = root.find('MsgId').text
                agent_id = root.find('AgentID').text
                print(to_user_name, from_user_name, create_time, msg_type, content, msg_id, agent_id)
            # return content

                # 被动回复
                create_time = timestamp = str(int(time.time()))
                content = chat(content).response#content.replace('吗', '').replace('?', '!').replace('？', '！')
                sReplyMsg = f'<xml><ToUserName>{to_user_name}</ToUserName><FromUserName>{from_user_name}</FromUserName><CreateTime>{create_time}</CreateTime><MsgType>text</MsgType><Content>{content}</Content><MsgId>{msg_id}</MsgId><AgentID>{agent_id}</AgentID></xml>'
                ret, sEncryptMsg = wxcpt.EncryptMsg(sReplyMsg, nonce, timestamp)
                if ret == 0:
                    pass
                else:
                    return 'ERR: EncryptMsg ret: ' + str(ret)
                return sEncryptMsg
        else:
            return 'ERR: DecryptMsg ret:' + str(ret)

@app.route('/robot2/', methods=['POST'])
def wechat_callback():
    # 获取消息内容
           
    data = request.data
    print(data)
    # ret, data = wxcpt.DecryptMsg(request.data, msg_signature, timestamp, nonce)
    # if ret !=0:
    #     return 'ERR: DecryptMsg ret:' + str(ret)
    xml_data = ET.fromstring(data)
    to_user_name = xml_data.find('ToUserName').text
    from_user_name = xml_data.find('FromUserName').text
    msg_type = xml_data.find('MsgType').text

    # 根据消息类型进行处理
    if msg_type == 'text':
        content = xml_data.find('Content').text
        response = generate_text_response(from_user_name, to_user_name, "你发送的消息是：" + content)
        return response
    else:
        return "success"

def generate_text_response(to_user, from_user, content):
    response = f"""
    <xml>
    <ToUserName><![CDATA[{to_user}]]></ToUserName>
    <FromUserName><![CDATA[{from_user}]]></FromUserName>
    <CreateTime>{int(time.time())}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
    </xml>
    """
    return response

# robot.config['HOST'] = '0.0.0.0'
# robot.config['PORT'] = 80
# robot.run()
app.run(host='0.0.0.0',port=80,debug=True)