# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

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
	return render(request, 'coordinator/projects.html', {
		'user': request.user, 
		'layout': layout
		})


def project(request, p_id):

	return render(request, 'coordinator/project.html', {
		'user': request.user, 
		'project_id': p_id
		})

