from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def nbsp(value):
	items = value.split('\n')
	result = ''
	for item in items:
		head = item.split('  ')[0]
		tail = item.split('  ')[-1]
		if len(head) > 10:
			head = head[:7] + '...'
		result = result + '<span>'+head+'</span><span class="right">'+tail+'</span> <br/>'
	return result

