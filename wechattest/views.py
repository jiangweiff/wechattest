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

@csrf_exempt
def fromwechat(request):
	if request.method == 'GET':
		signature = request.GET['signature']
 		timestamp = request.GET['timestamp']
 		nonce = request.GET['nonce']
 		echostr = request.GET['echostr'] or ""
 		return HttpResponse(echostr)
	else:
		root = ET.fromstring(request.body)
		touser = root.find('ToUserName').text
		fromuser = root.find('FromUserName').text
		root.find('ToUserName').text = fromuser
		root.find('FromUserName').text = touser
		reply = ET.tostring(root, encoding='utf-8')
		return HttpResponse(reply)