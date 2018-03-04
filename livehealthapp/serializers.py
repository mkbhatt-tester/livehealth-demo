# -*- coding: utf-8 -*-
from django.core import serializers
from django.http import HttpResponse
import json


# User Serializer
def user_serialize(obj,fmt,method,flg):
	# flg = 1=>login = true | 2=>register = true  
	if method=='POST' and flg=='1':
		return serializer(obj,fmt)
	elif method=='POST' and flg=='2':
		obj[0].save()
		obj[0].passwd='hidden' # Save & Hide The Password Field
		return serializer(obj,fmt)


# Note Serializer
def note_serialize(obj,fmt,method,flg):
	# flg = 1=>session = true  
	if method=='GET' and flg=='1':
		return serializer(obj,fmt)
	elif method=='POST' and flg=='1':
		return serializer(obj,fmt)


# Base Django Serializer
def serializer(obj,fmt):
	if fmt=='json':
		serialize_obj = serializers.serialize(fmt,obj)
		data = json.dumps({'status':'success','data':json.loads(serialize_obj)},indent=4)
		return HttpResponse(data,content_type="application/json",status=200)
	elif fmt=='xml':
		data = serializers.serialize(fmt,obj)
		return HttpResponse(data,content_type="application/xml",status=200)		
