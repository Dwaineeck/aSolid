from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
	def validateUser(self, post_data):

		is_valid = True
		errors = []

		if len(post_data.get('first_name')) < 2:
			is_valid = False
			errors.append('First Name > than 2 characters.')
		if len(post_data.get('last_name')) < 2:
			is_valid = False
			errors.append('Last Name > than 2 characters.')
		if len(post_data.get('email')) < 1:
			is_valid = False
			errors.append('Email is required.')
		elif not re.match('[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*@[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*(.[A-Za-z]{2,})', post_data.get('email')):
			is_valid = False
			errors.append('Must enter a valid email.')
		elif User.objects.filter(email=post_data['email']):
			is_valid = False
			errors.append('Email has been taken.')
		#if password >= 8 characters, matches password confirmation
		if len(post_data.get('password')) < 8:
			is_valid = False
			errors.append('Password >= 8 characters.')
		if post_data.get('password_confirmation') != post_data.get('password'):
			is_valid = False
			errors.append('Passwords do not match')

		return (is_valid, errors)

class User(models.Model):
	first_name = models.CharField(max_length = 45)
	last_name = models.CharField(max_length = 45)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	add = models.ManyToManyField("Job", related_name="add")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

	def __str__(self):
		return "first_name:{}, last_name:{}, email:{}, password:{}, add:{}, created_at:{}, updated_at:{}".format(self.first_name, self.last_name, self.email, self.password, self.created_at, self.updated_at)

class JobManager(models.Manager):
	def validateJob(self, post_data):

		is_valid = True
		errors = []

		if len(post_data.get('job')) < 3:
			is_valid = False
			errors.append('Job Title must be more than 3 characters.')
		if len(post_data.get('description')) < 10:
			is_valid = False
			errors.append('Description must be more than 10 characters.')
		if len(post_data.get('location')) < 1:
			is_valid = False
			errors.append('Must have a location.')
		return (is_valid, errors)
	def validateJobUpdate(self, post_data):

		is_valid = True
		errors = []

		if len(post_data.get('job')) < 2:
			is_valid = False
			errors.append('Job Title must be more than 3 characters.')
		if len(post_data.get('description')) < 2:
			is_valid = False
			errors.append('Description must be more than 10 characters.')
		if len(post_data.get('location')) < 1:
			is_valid = False
			errors.append('Must have a location.')

		return (is_valid, errors)

class Job(models.Model):
	description = models.CharField(max_length = 255)
	job = models.CharField(max_length = 255)
	location = models.CharField(max_length = 255)
	poster = models.ForeignKey(User, related_name = 'creator_jobs')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = JobManager()

	def __str__(self):
		return 'description:{}, job:{}'.format(self.description, self.user)






