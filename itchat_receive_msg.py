#coding=utf8
import itchat
from itchat.content import *
import os
import time

# 自动回复
# 封装好的装饰器，当接收到的消息是Text，即文字消息
def find_friend(nick_name):
    for people in itchat.get_friends(update= True):
        if people['NickName'] == nick_name:
            return people
              

@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
    #return(msg['Text'])  #自动回复给原用户
    contact = itchat.get_friends()
    #print(contact[0])
   #print('====================')
    #print(msg)
    if not msg['FromUserName'] == contact[0]['UserName']:
        itchat.send_msg((time.strftime("%H:%M:%S",time.localtime()) + u" - Joy 收到信息：发自 " \
                                    + msg['User']['NickName'] + ': '+msg['Text']), \
                                     toUserName= Kai_User['UserName'])

@itchat.msg_register([PICTURE,RECORDING,ATTACHMENT,VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
   # return '@%s@%s'%({'Picture':'img','Video':'vid'}.get(msg['Type'],'fil'),msg['FileName']) #自动回复到 发消息用户
    itchat.send('@img@%s' % msg['FileName'] ,toUserName= Kai_User['UserName'] ) #转发到 Ma Kai


    
#@itchat.msg_register([TEXT,PICTURE,CARD,MAP,SHARING,RECORDING,])  # 用下面的方法重新实现，收到消息会用下面方法处理
#def text_reply(msg):
    # 接收消息，分析，回复或者处理
    #if msg['ToUserName'] == 'filehelper':
    #    if msg['Text'].strip()== 'Open':
    #        os.system("start notepad.exe")
    #if msg['User']['NickName'] == 'Joy':
    #    itchat.send(time.strftime("%H:%M:%S",time.localtime())+': Got msg from Joy', toUserName='filehelper')

    #print(Kai_User)
    #print(msg)
    #if msg['MsgType'] == 1:    # Text msg
    #       itchat.send_msg((time.strftime("%H:%M:%S",time.localtime()) + u" - Joy 收到信息：发自 " \
     #                               + msg['User']['NickName'] + ': '+msg['Text']), \
      #                               toUserName= Kai_User['UserName'])
    #if msg['MsgType'] == 3:  # picture

   # if msg['MsgType'] == 42:  # name card
   # if msg['MsgType'] == 34:  # recording
   # if msg['MsgType'] == 49:  # file attachment
    #if msg['MsgType'] == 62  #video

    
   # if not msg['FromUserName'] == myUserName:
        # 发送一条提示给文件助手
    #    itchat.send_msg((u"收到好友的信息："+msg['FromUserName']+msg['User']['NickName']+msg['Text']), 'filehelper')
     #   print(msg['User'])
        # 回复给好友
      #  return u'[自动回复]您好，我现在有事不在，一会再和您联系。\n已经收到您的的信息：%s\n' % (msg['Text'])

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    Kai_User = find_friend('Ma Kai')
    
    # 获取自己的UserName
    # myUserName = itchat.get_friends(update=True)[0]["UserName"]
   # itchat.send("Hello World!", toUserName='filehelper')
   # itchat.send("@fil@%s" % 'test.xlsx', toUserName='filehelper')
   # itchat.send("@img@%s" % 'sushiplate.jpg', toUserName='filehelper')
    itchat.run()
   # itchat.send('Open', toUserName='filehelper')
    
    
    
