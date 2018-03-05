# -*- coding: utf-8 -*-
from django.http import HttpResponse
from livehealthapp.models import User,Note
from serializers import *
import hashlib
import re

# Serializer Format
fmt='json'


# User | RESTful View | returns : JSON Data
def users(request,fmt=fmt):
	try:

		# Validate Input
		if not re.match(r'^[\w]+$', str(request.POST.get('username')) ):
			raise Exception('Validation Failure : Only Alphanumeric Characters Allowed!')
		elif request.POST.get('register_flg')=='2' or request.POST.get('login_flg')=='1':
			if len(request.POST.get('passwd'))<3 or len(request.POST.get('username'))<3:
				raise Exception('Validation Failure : Username/Password Fields Minimum Length Must be Of 6 Characters!')

		# POST | Register User
		if request.POST.get('register_flg')=='2' and request.method=='POST':

			# convert pass to md5 string and save to db
			obj=User(username=request.POST.get('username'), passwd=hashlib.md5(str(request.POST.get('passwd',0))).hexdigest() )
			return user_serialize([obj],fmt,'POST','2')

		# POST | Login User
		elif request.POST.get('login_flg')=='1' and request.method=='POST':
			request.session.set_test_cookie()
			if request.method == 'POST':
				if request.session.test_cookie_worked(): # Check If Cookies Are Enabled 
					request.session.delete_test_cookie()
					obj = User.objects.get(username=request.POST.get('username'), passwd=hashlib.md5(str(request.POST.get('passwd',0))).hexdigest() )
					obj.passwd='hidden' # Hide The Password Field
					
					if request.POST.get('remember_flag')!='1':
						request.session.set_expiry(1800) # Log out after 30 min | if remember flag off
						
					request.session['session_id']=obj.id
					request.session['session_username']=obj.username
					request.session['session_set']='1'
					return user_serialize([obj],fmt,'POST','1')
			else:
				return HttpResponse("Please enable cookies and try again.",content_type="text/html",status=400)

		# GET | User Search & Select For Share
		elif request.GET.get('search') and request.session.get('session_set')=='1' and request.method=='GET':
			try:
				obj = User.objects.get(username__contains=request.GET.get('search'))
				obj.passwd='hidden'
				data = {'id':obj.id,'name':obj.username}
			except:
				data = {'id':0,'name':'Username Not Found'}
			return HttpResponse(json.dumps(data),content_type="application/json",status=200)

	except Exception,e:
		data = json.dumps({'status':'fail','message':str(e)},indent=4)
		return HttpResponse(data,content_type="application/json",status=400)



# Note | RESTful View | returns : JSON Data
def notes(request,fmt=fmt):
	
	try:
		default_shared_with = str(request.session.get('session_id'))+','

		# Validate Input
		if not (re.match(r'^[\w ]+$', str(request.POST.get('note_title')) ) or re.match(r'^[\w]+$', str(request.POST.get('note_body')) ) ):
			raise Exception('Validation Failure : Only Alphanumeric Characters Allowed!')
		elif request.POST.get('action')=='create' or request.POST.get('action')=='update':
			if len(request.POST.get('note_title'))<6 or len(request.POST.get('note_body'))<6:
				raise Exception('Validation Failure : Note Title/Note Content Fields Minimum Length Must be Of 6 Characters!')

		# POST | Create Note
		if request.POST.get('action')=='create' and request.POST.get('note_title') and request.POST.get('note_body') and request.session.get('session_set')=='1' and request.method=='POST':
			obj = User.objects.get(pk=int(request.session.get('session_id')))
			obj.note_set.create(note_title=request.POST.get('note_title'),note_body=request.POST.get('note_body'),shared_with=str(request.session.get('session_id'))+',')
			obj = Note.objects.get(note_title=request.POST.get('note_title'))
			return note_serialize([obj],fmt,'POST','1')

		# GET | Delete Note
		elif request.GET.get('action')=='delete' and request.session.get('session_set')=='1' and request.method=='GET':
			obj = Note.objects.get(pk=int(request.GET.get('note_id')))
			if obj.note_id==request.session.get('session_id'):
				obj.delete()
				return note_serialize([obj],fmt,'GET','1')
			else:
				raise Exception("You Do Not Have Ownership To Perform The Requested Action !")
		
		# POST | Share Note
		elif request.POST.get('action')=='share' and request.POST.get('share_id') and  request.session.get('session_set')=='1' and request.method=='POST':
			obj = Note.objects.get(pk=int(request.POST.get('note_id')))
			
			if request.POST.get('share_id') in obj.shared_with:
				raise Exception("Note Already Shared With The Current User !")

			obj.shared_with=obj.shared_with+request.POST.get('share_id')+','
			obj.save()
			return note_serialize([obj],fmt,'POST','1')

		# POST | Update Note
		elif request.POST.get('action')=='update' and request.POST.get('note_title') and  request.session.get('session_set')=='1' and request.method=='POST':
			obj = Note.objects.get(pk=int(request.POST.get('id')))
			if obj.note_id==request.session.get('session_id'):
				obj.note_title= request.POST.get('note_title')
				obj.note_body = request.POST.get('note_body')
				obj.save()
				return note_serialize([obj],fmt,'GET','1')
			else:
				raise Exception("You Do Not Have Ownership To Perform The Requested Action !")

		# GET | Get Notes ( Including Shared One For Logged In User | DESC )
		elif request.session.get('session_set')=='1' and request.method=='GET':
			obj=Note.objects.filter(shared_with__contains=request.session.get('session_id')).order_by('-id')
			return note_serialize(obj,fmt,'GET','1')


	except Exception,e:
		data = json.dumps({'status':'fail','message':str(e)},indent=4)
		return HttpResponse(data,content_type="application/json",status=400)