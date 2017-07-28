from django import template
from django.utils.safestring import mark_safe
from coordinator import models

register = template.Library()

@register.filter()
def nbsp(value):
	items = value.split('\n')
	result = ''
	for item in items:
		head = item.split('  ')[0]
		short_head = head
		tail = item.split('  ')[-1]
		if len(short_head) > 10:
			short_head = head[:7] + '...'
		result = result + '<span class="tooltipped" data-position="bottom" data-delay="20" data-tooltip="'+head+'">'+short_head+'</span><span class="right">'+tail+'</span> <br/>'
	return result

@register.filter()
def compare(value, arg):
	if value.find(arg) != -1:
		return True
	return False

@register.filter()
def comparecol(value, arg):
	return value.split('-')[-1] == arg

@register.filter()
def names(value, length):
	length = int(length)
	result = '<ul class="algo-list">'
	for item in value:
		result = result + '<li class="algo-item">'+item.name+'</li>'
		if length == 0:
			break
		length = length - 1
	result = result + '</ul>'
	return result

@register.filter()
def experiments(value, length=5):
	exps = models.Experiment.objects.filter(dataset=value)
	result = '<ul class="algo-list">'
	for item in exps:
		result = result + '<li class="algo-item">'+item.name+'</li>'
		if length == 0:
			break
		length = length - 1
	result = result + '</ul>'
	return result

