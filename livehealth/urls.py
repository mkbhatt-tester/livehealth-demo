
# APP ROUTES

from django.conf.urls import url, include
from django.contrib import admin
from livehealthapp import views


urlpatterns = [

	# VIEW ROUTE
	url(r'^$',views.index,name='index'),
	url(r'^dashboard$',views.dashboard,name='dashboard'),
	url(r'^logout$',views.logout,name='logout'),

	# RESTful ROUTE
    url(r'^users$',views.users,name='users'),
    url(r'^notes$',views.notes,name='notes'),


]