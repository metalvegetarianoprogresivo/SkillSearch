from django import template
from django.contrib.auth.models import Group 

register = template.Library()

def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

@register.filter(name='has_group') 
def has_group(user, group_name):
    print(group_name)
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all()