from socialnetwork.models import Post, Tag
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django import template
from django.template.defaultfilters import stringfilter

import re

register = template.Library()

	
@register.filter
@stringfilter
def link_tags(value):
	value = re.sub(r'(?:^|(?<=\s))@(\w+)', profile_link, value)
	value = re.sub(r'(?:^|(?<=\s))#(\w+)', tag_link, value)

	return value


def profile_link(match):
	tag = match.group()
	url = reverse('profile',args=[match.group(1)])

	return '<a href="%s">%s</a>' % (url,tag)

def tag_link(match):
	tag = match.group()
	url = reverse('tag',args=[match.group(1)])

	return '<a href="%s">%s</a>' % (url,tag)