# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# MODELS (USER,NOTE)

class User(models.Model):
	username = models.CharField(max_length=10,unique=True)
	passwd = models.CharField(max_length=50)
	created_at = models.DateTimeField(auto_now_add=True)

class Note(models.Model):
	note = models.ForeignKey(User)
	note_title = models.CharField(max_length=50,unique=True)
	note_body = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	shared_with = models.TextField()
