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
	f1_score = models.FloatField(default = 0)
	total_time_spent = models.FloatField(default = 0) # Seconds Time Delta

	def __str__(self):
		return self.name

class Experiment(models.Model):
	name = models.CharField(max_length=50)
	dataset = models.ForeignKey(DataSet)
	validation = models.CharField(max_length=20)
	validation_param = models.CharField(max_length=10)
	description = models.TextField()
	autogroup = models.BooleanField(default=False)
	algorithms = models.TextField()
	metric = models.CharField(max_length=50)
	timelimit = models.IntegerField()
	project = models.ForeignKey(Project)
	model_count = models.IntegerField(default=0)

	def __str__(self):
		return self.name

class EModel(models.Model):
	uuid = models.CharField(max_length=50)
	algorithm = models.CharField(max_length=255)
	algorithm_param = models.CharField(max_length=255)
	dataset = models.ForeignKey(DataSet)
	column = models.CharField(max_length=255)
	experiment = models.ForeignKey(Experiment, default=1)
	status = models.CharField(max_length=50, default="Initiated")

	def __str__(self):
		return self.uuid

