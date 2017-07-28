from __future__ import absolute_import, unicode_literals
from celery import shared_task
import random

@shared_task
def add(x, y):
    return x + y

@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def experiment(param):
	print param

	result = {
		'f1_score': random.random(), 
		'total_time_spent': random.random() # Time Delta with Seconds
	}
	return result

@shared_task
def predict(param):
	print param

	result = {
		'algorithm_id': 'ae4989-389984-9984	',
		'algorithm': 'Random Forest', 
		'prediction': '5-fold', 
		'prediction_score': '48', 
		'time': '1:18:19', 
		'download_link': 'downloadfile'
	}

	return result

@shared_task
def model_feature(param):
	print param

	y_list = []
	x_list = range(0,10)
	for i in x_list:
		y_list.append(random.random())
	result = {
		'x': x_list, 
		'y': y_list
	}

	return result
