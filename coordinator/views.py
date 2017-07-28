# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from coordinator import models
import json

# Create your views here.

@login_required
def index(request):
	projects = []
	if request.user.is_superuser:
		projects = models.Project.objects.all()
	else:
		projects = models.Project.objects.filter(owner = request.user)
	datasets = models.DataSet.objects.filter(project__in = projects)
	experiments = models.Experiment.objects.filter(project__in = projects)
	emodels = models.EModel.objects.filter(experiment__in = experiments)
	return render(request, 'coordinator/dashboard.html', {
		'user': request.user, 
		'projects': projects, 
		'datasets': datasets, 
		'experiments': experiments, 
		'emodels': emodels
		})

@login_required
def projects(request):
	projects = []
	layout = request.GET.get('layout')
	if layout != 'list':
		layout = 'grid'
	else:
		layout = 'list'
	query = request.GET.get('query')

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

	if request.user.is_superuser:
		if query:
			projects = models.Project.objects.filter(name__contains=query)
		else:
			projects = models.Project.objects.all()
	else:
		if query:
			projects = models.Project.objects.filter(Q(owner=request.user) | Q(visibility__contains='Public') & Q(name__contains=query))
		else:
			projects = models.Project.objects.filter(Q(owner=request.user) | Q(visibility__contains='Public'))

	return render(request, 'coordinator/projects.html', {
		'user': request.user, 
		'layout': layout, 
		'projects': projects, 
		'query': query
		})

@login_required
def project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	datasets = models.DataSet.objects.filter(project = project)

	experiments = models.Experiment.objects.filter(project = project)

	emodels = models.EModel.objects.filter(experiment__in = experiments)

	return render(request, 'coordinator/project.html', {
		'user': request.user, 
		'project_id': p_id,
		'project': project, 
		'datasets': datasets, 
		'experiments': experiments, 
		'emodels': emodels
		})

