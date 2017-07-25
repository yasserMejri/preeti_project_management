# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def data_sources_project(request, p_id):

	return render(request, 'coordinator/project-detail/data-sources.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'data-sources'
		})

def preview_project(request, p_id):

	return render(request, 'coordinator/project-detail/preview.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'preview'
		}) 

def experiments_project(request, p_id):

	return render(request, 'coordinator/project-detail/experiments.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'experiments'
		}) 

def results_project(request, p_id):

	return render(request, 'coordinator/project-detail/results.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'results'
		}) 

def predict_project(request, p_id):

	return render(request, 'coordinator/project-detail/predict.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'predict'
		}) 

def feature_project(request, p_id):

	return render(request, 'coordinator/project-detail/feature.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'feature'
		}) 

def deploy_project(request, p_id):

	return render(request, 'coordinator/project-detail/deploy.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'deploy'
		}) 

def api_project(request, p_id):

	return render(request, 'coordinator/project-detail/api.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'api'
		}) 

