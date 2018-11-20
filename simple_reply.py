#!/usr/bin/python
#coding=utf-8
import itchat
from itchat.content import *

@itchat.msg_register([TEXT])
def simple_reply(msg):
    if msg['Type'] == TEXT:
        ReplyContent = 'I received message: '+msg['Content']
    user = itchat.search_friends(name='Ma Kai')
    itchat.send_msg(ReplyContent,user[0]['UserName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
     if msg['isAt']:
        # print(msg) 
         itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'],\
                                                  msg['Content']), msg['FromUserName'])

itchat.auto_login(hotReload=True)
itchat.run()


