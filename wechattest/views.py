# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import xml.etree.ElementTree as ET

from wechatservice import WechatService

# Create your views here.
def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #print WechatService.GetAccessToken()
    context = {'latest_question_list': WechatService.GetUserList()}
    return render(request, 'wechattest/index.html', context)

def showqrcode(request):
	qrcode = WechatService.GetQrCode()
	return render(request, 'wechattest/showqrcode.html',{'qrcode':qrcode})

def createReplyMsg(touser, fromuser, msg):
	root = ET.Element('xml')
	ET.SubElement(root, 'ToUserName').text = touser
	ET.SubElement(root, 'FromUserName').text = fromuser
	ET.SubElement(root, 'MsgType').text = 'text'
	ET.SubElement(root, 'Content').text = msg
	ET.SubElement(root, 'CreateTime').text = '123456'
	ET.SubElement(root, 'MsgId').text = '1'
	return ET.tostring(root, encoding='utf-8')

def processWeChatPost(xmlbody):
	root = ET.fromstring(xmlbody)
	msgtype = root.find('MsgType').text
	touser = root.find('ToUserName').text
	fromuser = root.find('FromUserName').text
	if msgtype == 'text':
		return createReplyMsg(fromuser, touser, 'reply : '+root.find('Content').text)
	elif msgtype == 'event':
		root.find('ToUserName').text = fromuser
		root.find('FromUserName').text = touser
		return createReplyMsg(fromuser, touser, 'event : {} {}'.format(root.find('Event').text, root.find('EventKey').text))
	else:
		return createReplyMsg(fromuser, touser, 'unknown event')

@csrf_exempt
def fromwechat(request):
	if request.method == 'GET':
		signature = request.GET['signature']
 		timestamp = request.GET['timestamp']
 		nonce = request.GET['nonce']
 		echostr = request.GET['echostr'] or ""
 		return HttpResponse(echostr)
	else:
		reply = processWeChatPost(request.body)
		print reply
		return HttpResponse(reply)