# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from datetime import datetime
from coordinator import models
from reportWriter import parse_file
import json
import re
import sys
from StringIO import StringIO
import numpy as np
import uuid
import random

from tasks import experiment
from tasks import predict
from tasks import model_feature

# Create your views here.


all_params = []
l_params = []
l_algo = ''
l_dataset = None
l_column = ''

def loop_params(exp, depth):
	global l_params, l_algo, l_dataset, l_column, all_params
	if depth == len(all_params):
		emodel = models.EModel(
			uuid = uuid.uuid4(), 
			algorithm = l_algo, 
			algorithm_param = l_params, 
			dataset = l_dataset, 
			column = l_column, 
			experiment= exp
			)
		emodel.save()
		return
	for param in all_params[depth]['param_data']:
		l_params.append({
			all_params[depth]['param_name']: param
			})
		loop_params(exp, depth + 1)
		l_params = l_params[:-1]



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

	datasets = models.DataSet.objects.filter(project=project)

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
		'parse_result': parse_result, 
		'datasets': datasets
		})

def preview_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	datasets = models.DataSet.objects.filter(project=project)
	data = None
	options = ['ID', 'Feature', 'ML', 'Rules']
	cols = []
	rowcount = colcount = 0

	dataset_id = request.GET.get('dataset')
	if dataset_id is None:
		try:
			dataset_id = datasets[0].id
		except:
			pass

	try:
		dataset = models.DataSet.objects.get(id=int(dataset_id))
		data = json.loads(dataset.column_data)
		rowcount = dataset.rowcount
		colcount = dataset.colcount
		cols = [item['column_name'] for item in data]
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
		'colcount': colcount,
		'cols': cols
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

def create_models(exp):
	global l_params, l_algo, l_dataset, l_column, all_params
	mls  = []

	a = json.loads(exp.dataset.column_data)
	for item in a:
		if item['usuage'] == 'ML' or item['usuage'].find('Rule') != -1:
			mls.append(item['column_name'])
	algos = json.loads(exp.algorithms)
	for algo in algos:
		all_params = []
		for param_key in algos[algo]:
			if param_key == 'optimize':
				continue
			all_params.append({
				'param_name': param_key, 
				'param_data': algos[algo][param_key].split(',')
				})
		l_algo = algo
		l_dataset = exp.dataset
		for column in mls:
			l_column = column
			loop_params(exp, 0)



@login_required
def experiments_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	data = get_algorigthm()

	if request.method == 'POST':
		print request.POST
		algo = {}
		for key in request.POST:
			if request.POST.get(key) == 'on' and key.find('autogroup') == -1:
				algo[key] = {}
		for key in algo:
			for subkey in request.POST:
				if subkey.find(key) != -1 and subkey != key:
					tp = request.POST.getlist(subkey)
					if len(tp) != 1:
						algo[key][subkey.replace(key+'-', '')] = ','.join(tp)
					else:
						algo[key][subkey.replace(key+'-', '')] = tp[0]


		v_param = request.POST.get('validator-idx') if request.POST.get('validation') == 'Seperate Dataset' else request.POST.get('validation-parameter')

		exp = models.Experiment(
			name = request.POST.get('name'), 
			dataset = models.DataSet.objects.get(id=int(request.POST.get('traindata'))), 
			validation = request.POST.get('validation'), 
			validation_param = v_param, 
			description = request.POST.get('description'), 
			autogroup = True if request.POST.get('autogroup') else False, 
			algorithms = json.dumps(algo), 
			metric = request.POST.get('metric'), 
			timelimit = request.POST.get('timelimit'), 
			project = project
		)
		exp.save()

		create_models(exp)

		exp.model_count = len(models.EModel.objects.filter(experiment = exp))
		exp.save()

		message = {}
		message['file'] = {
			'name': exp.dataset.file.name, 
			'path': exp.dataset.file.path
		}
		message['columns'] = exp.dataset.column_data
		message[exp.validation] = exp.validation_param
		message['algorithm'] = algo
		message['metric'] = exp.metric
		message['timelimit'] = exp.timelimit

		result = experiment.delay(message)
		# exp.f1_score = result['f1_score']
		# exp.total_time_spent = result['total_time_spent']

		exp.save()


	datasets = models.DataSet.objects.filter(project = project)

	experiments = models.Experiment.objects.filter(project = project)

	validators = models.DataSet.objects.filter(project = project, scope="Validate")

	return render(request, 'coordinator/project-detail/experiments.html', {
		'user': request.user, 
		'project': project, 
		'project_id': p_id, 
		'page_name': 'experiments',
		'datasets': datasets, 
		'experiments': experiments, 
		'algorithms': data, 
		'validators': validators
		}) 

@login_required
def results_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	experiments = models.Experiment.objects.filter(project = project)
	active_idx = None
	emodels = []

	try:
		active_idx = experiments[0].id
		if request.GET.get('experiment'):
			active_idx = int(request.GET.get('experiment'))
	except:
		pass

	statuses = ['Done', 'Learning', 'Initiated', 'Error']

	cur_status = request.GET.get('status')
	try:
		if cur_status and cur_status != 'all':
			emodels = models.EModel.objects.filter(experiment = models.Experiment.objects.get(id=active_idx), status=cur_status)
		else:
			emodels = models.EModel.objects.filter(experiment = models.Experiment.objects.get(id=active_idx))
	except:
		pass

	return render(request, 'coordinator/project-detail/results.html', {
		'user': request.user, 
		'project': project, 
		'project_id': p_id, 
		'page_name': 'results',
		'experiments': experiments, 
		'emodels': emodels, 
		'statuses': statuses, 
		'active_idx': active_idx, 
		'cur_status': cur_status
		}) 

@login_required
def predict_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	if request.method == 'POST':
		if request.POST.get('action') == 'compute':
			input_file = request.FILES['input-file']
			dest = open(settings.BASE_DIR+'/TEMP/'+input_file.name, 'w+')
			for chunk in input_file:
				dest.write(chunk)
			dest.close()
			emodel = models.EModel.objects.get(id=int(request.POST.get('model-id')))
			column_data = json.loads(emodel.dataset.column_data)
			feature_column = None
			for cl in column_data:
				if cl['usuage'] == 'Feature':
					feature_column = cl['column_name']
					break
			target_column = emodel.column
			message = {
				'uuid': emodel.uuid, 
				'feature_column': feature_column, 
				'target_column': target_column, 
				'dataset_file': emodel.dataset.file.path, 
				'input_file': settings.BASE_DIR+'/TEMP/'+input_file.name
			}
			result = predict.delay(message)
			result = result.get()

			result['download_link'] = static(result['download_link'])

			return HttpResponse(json.dumps({
				'status': 'success', 
				'result': result
				}))

	experiments = models.Experiment.objects.filter(project = project)
	active_idx = None
	emodels = []

	try:
		active_idx = experiments[0].id
		if request.GET.get('experiment'):
			active_idx = int(request.GET.get('experiment'))
	except:
		pass

	statuses = ['Done', 'Learning', 'Initiated', 'Error']

	cur_status = request.GET.get('status')
	try:
		if cur_status and cur_status != 'all':
			emodels = models.EModel.objects.filter(experiment = models.Experiment.objects.get(id=active_idx), status=cur_status)
		else:
			emodels = models.EModel.objects.filter(experiment = models.Experiment.objects.get(id=active_idx))
	except:
		pass

	return render(request, 'coordinator/project-detail/predict.html', {
		'user': request.user, 
		'project': project, 
		'project_id': p_id, 
		'page_name': 'predict', 
		'experiments': experiments, 
		'emodels': emodels, 
		'statuses': statuses, 
		'active_idx': active_idx, 
		'cur_status': cur_status
		}) 

@login_required
def feature_project(request, p_id):

	project = models.Project.objects.get(id=p_id)

	if request.method == 'POST':
		if request.POST.get('action') == 'get_model_chart':
			emodel = models.EModel.objects.get(id=int(request.POST.get('model-id')))
			message = {
				'uuid': emodel.uuid
			}
			result = model_feature.delay(message)
			result = result.get()

			return HttpResponse(json.dumps({
				'status': 'success', 
				'result': result
				}))

	experiments = models.Experiment.objects.filter(project = project)
	active_idx = None
	emodels = []

	try:
		active_idx = experiments[0].id
		if request.GET.get('experiment'):
			active_idx = int(request.GET.get('experiment'))
	except:
		pass

	statuses = ['Done', 'Learning', 'Initiated', 'Error']

	cur_status = request.GET.get('status')
	try:
		if cur_status and cur_status != 'all':
			emodels = models.EModel.objects.filter(experiment = models.Experiment.objects.get(id=active_idx), status=cur_status)
		else:
			emodels = models.EModel.objects.filter(experiment = models.Experiment.objects.get(id=active_idx))
	except:
		pass

	return render(request, 'coordinator/project-detail/feature.html', {
		'user': request.user, 
		'project': project, 
		'project_id': p_id, 
		'page_name': 'feature', 
		'experiments': experiments, 
		'emodels': emodels, 
		'statuses': statuses, 
		'active_idx': active_idx, 
		'cur_status': cur_status
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

