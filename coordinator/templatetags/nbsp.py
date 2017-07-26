from django import template
from django.utils.safestring import mark_safe

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
