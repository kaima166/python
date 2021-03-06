#coding=utf-8
import itchat
from itchat.content import TEXT
from itchat.content import *
import sys
import time
import re
import os
msg_information = {}
face_bug=None #针对表情包的内容

# 其中isFriendChat表示好友之间，isGroupChat表示群聊，isMapChat表示公众号
# 收到群消息后，记录下来
@itchat.msg_register([TEXT,PICTURE,FRIENDS,CARD,MAP,SHARING,RECORDING,ATTACHMENT],isFriendChat=True,isGroupChat=True)
def receive_msg(msg):
  # ActualNickName : 实际 NickName(昵称) 群消息里(msg)才有这个值
  if 'ActualNickName' in msg:
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) #接收消息的时间
    if msg['isAt']:   # 如果有人 @ 发消息， FromUserName 是群的ID，ActualNick 是群里的发送者的昵称
        # print(msg)
         itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'],\
                                                msg['Content']), msg['FromUserName'])
          
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
  #否则的话是属于个人朋友的消息
  else:
    if itchat.search_friends(userName=msg['FromUserName'])['RemarkName']:#优先使用备注名称
      msg_from = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']
    else:
      msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName'] #在好友列表中查询发送信息的好友昵称
    group_name = ""
  msg_time = msg['CreateTime'] #信息发送的时间
  msg_id = msg['MsgId']  #每条信息的id
  msg_content = None   #储存信息的内容
  msg_share_url = None  #储存分享的链接，比如分享的文章和音乐
  # 如果发送的消息是文本或者好友推荐
  if msg['Type'] == 'Text' or msg['Type'] == 'Friends':
    msg_content = msg['Text']
  #如果发送的消息是附件、视频、图片、语音
  elif msg['Type'] == "Attachment" \
      or msg['Type'] == 'Picture' \
      or msg['Type'] == 'Recording':
    msg_content = msg['FileName']  #内容就是他们的文件名
    #msg_content = "F:\\weixininfo\\"+msg['FileName']
    msg['Text'](str(msg_content))  #下载文件
  elif msg['Type'] == 'Sharing':   #如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
    msg_content = msg['Text']
    msg_share_url = msg['Url']    #记录分享的url

  face_bug = msg_content
  #将信息存储在字典中，每一个msg_id对应一条信息
  time.sleep(2)
  msg_information.update(
    {
      msg_id: {
        "msg_from": msg_from,
        "msg_time": msg_time,
        "msg_time_rec": msg_time_rec,
        "msg_type": msg["Type"],
        "msg_content": msg_content,
        "msg_share_url": msg_share_url,
        "group_name":group_name,
       }
    }
  )
  #自动删除130秒之前的消息，避免数据量太大后引起内存不足
  del_info = []
  for k in msg_information:
    m_time = msg_information[k]['msg_time'] #取得消息时间
    if int(time.time()) - m_time > 130:
      del_info.append(k)
  if del_info:
    for i in del_info:
      msg_information.pop(i)
  #print(msg_information)
  
itchat.auto_login(hotReload=True)
itchat.run()
