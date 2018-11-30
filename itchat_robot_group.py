#coding=utf8
import requests
import itchat
from itchat.content import TEXT
from itchat.content import *
import sys
import time
import re
import os

# KEY = '8edce3ce905a4c1dbb965e6b35c3834d'
KEY = '265e8f716d9d4686953d9de4f2adf9cf'
global robot_mode, robot_start
robot_mode =0

def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据，这是个机器人试验
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : '349594', #'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return

@itchat.msg_register([TEXT,PICTURE,FRIENDS,CARD,MAP,SHARING,RECORDING,ATTACHMENT],isFriendChat=True,isGroupChat=True)
def receive_msg(msg):
  # ActualNickName : 实际 NickName(昵称) 群消息里(msg)才有这个值
  global robot_mode, robot_start
  robot_start = 1
  if 'ActualNickName' in msg:   # 当群消息的时候
      if msg['isAt']:   # 如果有人 @ 发消息， FromUserName 是群的ID，ActualNick 是群里的发送者的昵称
          if "robot" in msg['Text']:
              robot_mode =1
              robot_start = 0
              itchat.send(u'@%s\u2005 Robot mode: %s' % (msg['ActualNickName'],\
                                                        "跟我聊天吧 :)"), msg['FromUserName'])
          if "over" in msg['Text']:
              robot_mode =0
              itchat.send(u'@%s\u2005 Robot mode: %s' % (msg['ActualNickName'],\
                                                        "很高兴跟你聊天 :) 再见！"), msg['FromUserName'])
          if robot_mode ==1 and robot_start ==1:
              reply = get_response(msg['Text'])
              itchat.send(u'@%s\u2005 Robot mode: %s' % (msg['ActualNickName'],\
                                                        reply), msg['FromUserName'])
  # 当不是 @ 消息
  
      from_user = msg['ActualUserName'] #群消息的发送者,用户的唯一标识
      msg_from = msg['ActualNickName']#发送者群内的昵称
      friends = itchat.get_friends(update=True)#获取所有好友
      for f in friends:
        if from_user == f['UserName']: #如果群消息是好友发的
          if f['RemarkName']: # 优先使用好友的备注名称，没有则使用昵称
            msg_from = f['RemarkName']
          else:
            msg_from = f['NickName']
          break
      groups = itchat.get_chatrooms(update=True)#获取所有的群
      for g in groups:
        if msg['FromUserName'] == g['UserName']:#根据群消息的FromUserName匹配是哪个群
          group_name = g['NickName']
          group_menbers = g['MemberCount']
          break
      group_name = group_name + "(" + str(group_menbers) +")"
  # 'ActualNickName' NOT in msg,非群消息
  
  
itchat.auto_login(hotReload=True)
itchat.run()
