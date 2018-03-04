# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader,RequestContext
from django.views.decorators.csrf import csrf_exempt
from restful_views import *
import hashlib
import json


# Views

# Index
def index(request):
	if request.session.get('session_id'):
		return redirect('dashboard')
	elif request.GET.get('register'):
		template = loader.get_template('index.html')
		return render(request,'index.html',{'register':'active'})
	else:
		template = loader.get_template('index.html')
		return render(request,'index.html',{'login':'active'})


# Dashboard
def dashboard(request):
	if request.session.get('session_id'):
		template = loader.get_template('dashboard.html')
		return render(request,'dashboard.html',{"username":request.session.get('session_username')})
	else:
		return redirect('/')


# Log Out
def logout(request):
	try:
		if request.method=="POST":
			del request.session['session_set']
			del request.session['session_id']
			del request.session['session_username']
			request.session.flush()
			data = json.dumps({'status':'success','message':'Logged Out!'},indent=4)
			return HttpResponse(data,content_type="application/json")
		else:
			raise Exception("Only Post Method Allowed !")
	except KeyError:
		pass

	except Exception,e:
		data = json.dumps({'status':'fail','message':str(e)},indent=4)
		return HttpResponse(data,content_type="application/json")
