# -*- coding: UTF-8 -*-
import itchat

def find_friend(nick_name):
	  for people in itchat.get_friends():
		  if people['NickName'] == nick_name:
			  print('good')
			  return people
		  else: return 0

                    
itchat.auto_login(hotReload=True)
  # friend =0
friend = find_friend('Ma Kai')
  #if friend !=0:
print(friend)
#itchat.send(msg='你好啊',toUserName=username)
itchat.logout()
