# 创建应用实例
import sys

from wxcloudrun import app



#robot = werobot.WeRoBot()#app_id='wx20b1396d77813bab',token='AAQ9G7sEAAABAAAAAAAZHBKxAjsPDrr0/hdLZiAAAAAraAdzKm8i8JwFJ68cDOJBtIHsmv3F8e00LCv7f+tYvrdcIYN+n7bDX7DzL30SBV0F41HP29O6/zzd24/PPjeAmEt1eV+92opWZoTZaYXE4803U3e+7eFwGqdjQCxZ5L6SFxz0e5v1XDMlpLF5mQd/oW6tQ3lCcFxS')
 
# @robot.text
# def hello_world():
#     return 'Hello World!'
# robot.config['HOST'] = '0.0.0.0'
# robot.config['PORT'] = 80
# #if __name__ == '__main__':
# robot.run()


# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])
