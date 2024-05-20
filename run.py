# 创建应用实例
import sys

#from wxcloudrun import app

# 启动Flask Web服务
#if __name__ == '__main__':
#    app.run(host=sys.argv[1], port=sys.argv[2])

import werobot
 
robot = werobot.WeRoBot(token='tokenhere')
 
@robot.text
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    robot.run()