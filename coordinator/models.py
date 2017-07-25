# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()
	visibility = models.CharField(max_length=10)
	task = models.CharField(max_length=20)
	category = models.CharField(max_length=20)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	created_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class DataSet(models.Model):
	file = models.FileField(upload_to='dataset')
	name = models.CharField(max_length=50)
	scope = models.CharField(max_length=50)
	parse_result = models.BooleanField(default=True)
	created_time = models.DateTimeField(auto_now=True)
	project= models.ForeignKey(Project, on_delete=models.CASCADE)
	column_data = models.TextField()
	rowcount = models.IntegerField()
	colcount = models.IntegerField()

	def __str__(self):
		return self.name

