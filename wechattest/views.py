# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from wechatservice import WechatService

# Create your views here.
def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #print WechatService.GetAccessToken()
    context = {'latest_question_list': WechatService.GetUserList()}
    return render(request, 'wechattest/index.html', context)