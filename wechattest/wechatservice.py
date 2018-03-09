# -*- coding: utf-8 -*-
import thread
import requests
import time
import logging

header = { "Content-Type" : "application/json",
	}

class WechatService:
	appID = 'wxa14e95d56761b3d3'
	appsecret = 'dd14523bb411d4cfb93645d95048e782'
	accesstoken = None
	mythread = None
	expires_t = 0

	# @staticmethod
	# def Init():
	# 	if WechatService.mythread == None:
	# 		WechatService.mythread = thread.start_new_thread(WechatService.CheckAccessToken, ())
	# 	print 'wechat service up'

	# @staticmethod
	# def CheckAccessToken():
	# 	expires_t = 0
	# 	while(1):
	# 		if time.time() >= expires_t:
	# 			page = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(WechatService.appID,WechatService.appsecret))
	# 			pagejson = page.json()
	# 			accesstoken = pagejson['access_token']
	# 			expires_t = time.time()+pagejson['expires_in']
	# 			print "accesstoken refreshed {} {}".format(accesstoken,expires_t)
	# 		time.sleep(10)

	@staticmethod
	def GetAccessToken():
		if time.time() >= WechatService.expires_t:
			page = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(WechatService.appID,WechatService.appsecret))
			pagejson = page.json()
			WechatService.accesstoken = pagejson['access_token']
			WechatService.expires_t = time.time()+pagejson['expires_in']-200
			print "accesstoken refreshed {} {}".format(WechatService.accesstoken,WechatService.expires_t)
		return WechatService.accesstoken
		# if WechatService.accesstoken == None:
		# 	raise Exception("WeChat accesstoken not available")
		# return WechatService.accesstoken

	@staticmethod
	def GetQrCode():
		tk = WechatService.GetAccessToken()
		page = requests.post('https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={}'.format(tk),
			{'expire_seconds': 604800, 'action_name': 'QR_SCENE', 'action_info': {'scene': {'scene_id': 123}}},
			headers = header)
		logging.getLogger('mylogger').debug(page.json())
		ticket = page.json()['ticket']
		page = requests.get('https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={}'.format(ticket))
		return page

	@staticmethod
	def GetUserList():
		tk = WechatService.GetAccessToken()
		page = requests.get('https://api.weixin.qq.com/cgi-bin/user/get?access_token={}&next_openid='.format(tk))
		pagejson = page.json()
		return pagejson['data']['openid']

