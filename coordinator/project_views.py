# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from coordinator import models
from reportWriter import parse_file
import json

# Create your views here.

@login_required
def data_sources_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	filename = filesize = dset_name = created_time = scope = owner = None
	parse_result = None
	if request.method == 'POST' and request.POST.get('add-new'):
		file = request.FILES['file']
		filename = file.name
		filesize = file.size
		dset_name = request.POST.get('dset_name')
		created_time = datetime.now()
		owner = request.user
		scope = 'Experiment'
		r = d = None
		rc = cc = 0
		if request.POST.get('validate'):
			scope = "Validate"
		try:
			r, d, cc, rc = parse_file(file)
			parse_result = 'Success'
		except:
			parse_result = 'Fail'

		if r == True:
			item = models.DataSet(
				file=file, 
				name = dset_name, 
				scope = scope, 
				parse_result = True,
				project = project, 
				column_data = json.dumps(d),
				rowcount = rc, 
				colcount = cc
				)
			item.save()

	return render(request, 'coordinator/project-detail/data-sources.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'data-sources', 
		'filename': filename, 
		'filesize': filesize, 
		'dset_name': dset_name, 
		'scope': scope, 
		'created_time': created_time,
		'owner': owner, 
		'parse_result': parse_result
		})

def preview_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	datasets = models.DataSet.objects.filter(project=project)
	data = None
	options = ["option1", "option2", "option3"]
	rowcount = colcount = 0

	dataset_id = request.GET.get('dataset')
	if dataset_id is None:
		dataset_id = 1

	try:
		dataset = models.DataSet.objects.get(id=int(dataset_id))
		data = json.loads(dataset.column_data)
		rowcount = dataset.rowcount
		colcount = dataset.colcount
	except:
		data = []

	print data
	print dataset_id

	return render(request, 'coordinator/project-detail/preview.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'preview', 
		'datasets': datasets, 
		'data': data, 
		'dataset_id': dataset_id, 
		'options': options, 
		'rowcount': rowcount, 
		'colcount': colcount
		}) 

@login_required
def preview_post_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	status = 'success'

	try:
		dataset = models.DataSet.objects.get(id=int(request.POST.get('dataset_id')))
		print "COLUMN DATA   "
		data = json.loads(dataset.column_data)
		print data
		idx = 0
		for item in data:
			if item['column_name'] == request.POST.get('column_name'):
				data[idx]['usuage'] = request.POST.get('data')
				break
			idx = idx + 1
		print "Modified -" * 20
		print data
		dataset.column_data = json.dumps(data)
		dataset.save()
	except:
		status = 'fail'
	return HttpResponse(json.dumps({
		'status': status,
		'request': request.POST
		}))

@login_required
def experiments_project(request, p_id):

	project = models.Project.object.get(id=p_id)

	return render(request, 'coordinator/project-detail/experiments.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'experiments'
		}) 

def results_project(request, p_id):

	project = models.Project.object.get(id=p_id)

	return render(request, 'coordinator/project-detail/results.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'results'
		}) 

def predict_project(request, p_id):

	project = models.Project.object.get(id=p_id)

	return render(request, 'coordinator/project-detail/predict.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'predict'
		}) 

def feature_project(request, p_id):

	project = models.Project.object.get(id=p_id)

	return render(request, 'coordinator/project-detail/feature.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'feature'
		}) 

def deploy_project(request, p_id):

	project = models.Project.object.get(id=p_id)

	return render(request, 'coordinator/project-detail/deploy.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'deploy'
		}) 

def api_project(request, p_id):

	project = models.Project.object.get(id=p_id)

	return render(request, 'coordinator/project-detail/api.html', {
		'user': request.user, 
		'project_id': p_id, 
		'page_name': 'api'
		}) 

