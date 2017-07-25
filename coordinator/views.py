# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from coordinator import models

# Create your views here.

@login_required
def index(request):
	return render(request, 'coordinator/dashboard.html', {
		'user': request.user
		})


def projects(request):
	layout = request.GET.get('layout')
	if layout != 'list':
		layout = 'grid'
	else:
		layout = 'list'

	if request.method == 'POST':
		project = models.Project(
				name = request.POST.get('name'), 
				description = request.POST.get('description'), 
				visibility = request.POST.get('visibility'), 
				task = request.POST.get('task'), 
				category = request.POST.get('category'), 
				owner = request.user
			)
		project.save()

	projects = models.Project.objects.all()

	return render(request, 'coordinator/projects.html', {
		'user': request.user, 
		'layout': layout, 
		'projects': projects
		})


def project(request, p_id):

	return render(request, 'coordinator/project.html', {
		'user': request.user, 
		'project_id': p_id
		})

