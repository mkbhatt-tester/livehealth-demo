# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
import hashlib
from livehealthapp.models import User,Note

class UserTestCase(TestCase):
	
	#  Test User,Note (Create)
	def setUp(self):

		user_a = User.objects.create(username="User1",passwd=hashlib.md5(str("Test 1")).hexdigest() )
		user_b = User.objects.create(username="User2",passwd=hashlib.md5(str("Test 2")).hexdigest() )

		user_a = User.objects.get(pk=user_a.id)
		user_a.note_set.create(note_title="Test Note 1",note_body="Test Body 1",shared_with='1'+',')

		user_b = User.objects.get(pk=user_b.id)
		user_b.note_set.create(note_title="Test Note 2",note_body="Test Body 2",shared_with='2'+',')

	
	#  Test User (GET)	
	def test_user_get(self):
		
		user_a = User.objects.get(username="User1")
		user_b = User.objects.get(username="User2")

		self.assertEqual(user_a.username, 'User1')
		self.assertEqual(user_b.username, 'User2')
		self.assertEqual(user_a.passwd,hashlib.md5(str("Test 1")).hexdigest())
		self.assertEqual(user_b.passwd,hashlib.md5(str("Test 2")).hexdigest())


	#  Test Note (GET)
	def test_note_get(self):
		
		user_a_note = Note.objects.get(note_title='Test Note 1')
		user_b_note = Note.objects.get(note_title='Test Note 2')

		self.assertEqual(user_a_note.note_title, 'Test Note 1')
		self.assertEqual(user_b_note.note_title, 'Test Note 2')
