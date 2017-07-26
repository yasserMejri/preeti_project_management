# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from coordinator import models
import json

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
		if request.POST.get('add-new'):
			project = models.Project(
				name = request.POST.get('name'), 
				description = request.POST.get('description'), 
				visibility = request.POST.get('visibility'), 
				task = request.POST.get('task'), 
				category = request.POST.get('category'), 
				owner = request.user
			)
			project.save()
		if request.POST.get('edit'):
			project = models.Project.objects.get(id=int(request.POST.get('project_id')))
			project.name = request.POST.get('name') 
			project.description = request.POST.get('description')
			project.visibility = request.POST.get('visibility')
			project.task = request.POST.get('task')
			project.category = request.POST.get('category')
			project.owner = request.user
			project.save()
		if request.POST.get('delete'):
			project = models.Project.objects.get(id=int(request.POST.get('project_id')))
			project.delete()
			return HttpResponse(json.dumps({
				'status': 'success', 
				'request': request.POST
				}))

	projects = models.Project.objects.filter(owner=request.user)

	return render(request, 'coordinator/projects.html', {
		'user': request.user, 
		'layout': layout, 
		'projects': projects
		})


def project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	return render(request, 'coordinator/project.html', {
		'user': request.user, 
		'project_id': p_id,
		'project': project
		})

