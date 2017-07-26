# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime
from coordinator import models
from reportWriter import parse_file
import json
import re
import sys
from StringIO import StringIO
import numpy as np

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
		'project': project, 
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
	options = ['ID', 'Feature', 'ML']
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

	return render(request, 'coordinator/project-detail/preview.html', {
		'user': request.user, 
		'project': project, 
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
		data = json.loads(dataset.column_data)
		idx = 0
		for item in data:
			if item['column_name'] == request.POST.get('column_name'):
				data[idx]['usuage'] = request.POST.get('data')
				break
			idx = idx + 1
		dataset.column_data = json.dumps(data)
		dataset.save()
	except:
		status = 'fail'
	return HttpResponse(json.dumps({
		'status': status,
		'request': request.POST
		}))

def print_to_variable(v):
    old_stdout = sys.stdout
    result = StringIO()
    sys.stdout = result
    print v
    sys.stdout = old_stdout
    return result.getvalue()

def get_algorigthm():
	data = ''
	with open(settings.BASE_DIR + '/extra_data/algorithm.data') as f:
		data = f.read()
	items = re.findall(r'np.arange\(.*\)', data)

	for item in items:
		tp = print_to_variable(eval(item)).replace('  ', ',')
		data = data.replace(item, tp)
	items = re.findall(r'range\(.*\)', data)

	for item in items:
		tp = print_to_variable(eval(item))
		data = data.replace(item, tp)
	items = re.findall(r'\d+e-\d+', data)
	for item in items:
		tp = print_to_variable(eval(item))
		data = data.replace(item, tp)
	items = re.findall(r'\d+\.', data)
	for item in items:
		tp = print_to_variable(eval(item))
		data = data.replace(item, tp)

	data = data.replace('\n','').replace('\t','').replace('\r','').replace('True', '"True"').replace('False', '"False"').replace(',]',']')

	return json.loads(data)

@login_required
def experiments_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	data = get_algorigthm()

	if request.method == 'POST':
		algo = {}
		for key in request.POST:
			if request.POST.get(key) == 'on' and key.find('autogroup') == -1:
				algo[key] = {}
		for key in algo:
			for subkey in request.POST:
				if subkey.find(key) != -1 and subkey != key:
					algo[key][subkey.replace(key+'-', '')] = request.POST.get(subkey)

		exp = models.Experiment(
			name = request.POST.get('name'), 
			dataset = models.DataSet.objects.get(id=int(request.POST.get('traindata'))), 
			validation = request.POST.get('validation'), 
			validation_param = request.POST.get('validation-parameter'), 
			description = request.POST.get('description'), 
			autogroup = True if request.POST.get('autogroup') else False, 
			algorithms = json.dumps(algo), 
			metric = request.POST.get('metric'), 
			timelimit = request.POST.get('timelimit'), 
			project = project
		)
		exp.save()


	datasets = models.DataSet.objects.filter(project = project)

	experiments = models.Experiment.objects.filter(project = project)

	return render(request, 'coordinator/project-detail/experiments.html', {
		'user': request.user, 
		'project': project, 
		'project_id': p_id, 
		'page_name': 'experiments',
		'datasets': datasets, 
		'experiments': experiments, 
		'algorithms': data
		}) 

@login_required
def results_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	return render(request, 'coordinator/project-detail/results.html', {
		'user': request.user, 
		'project': project, 
		'project_id': p_id, 
		'page_name': 'results'
		}) 

@login_required
def predict_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	return render(request, 'coordinator/project-detail/predict.html', {
		'user': request.user, 
		'project': project, 
		'project_id': p_id, 
		'page_name': 'predict'
		}) 

@login_required
def feature_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	return render(request, 'coordinator/project-detail/feature.html', {
		'user': request.user, 
		'project': project, 
		'project_id': p_id, 
		'page_name': 'feature'
		}) 

@login_required
def deploy_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	return render(request, 'coordinator/project-detail/deploy.html', {
		'user': request.user, 
		'project': project, 
		'project_id': p_id, 
		'page_name': 'deploy'
		}) 

@login_required
def api_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	return render(request, 'coordinator/project-detail/api.html', {
		'user': request.user, 
		'project': project, 
		'project_id': p_id, 
		'page_name': 'api'
		}) 

