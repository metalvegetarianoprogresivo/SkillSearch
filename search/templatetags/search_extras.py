from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def get_importance(*args, **kwargs):
    bold_strings = ""
    normal_strings = ""
    queryset, tags = args[0], args[1]
    queryset = queryset.split()
    temporary = []
    
    for skill in queryset:
        if '/' in skill:
            joined_skill = skill.split('/')
            for i in joined_skill:
                temporary.append(i)
        else:
            temporary.append(skill)

    for skill in temporary:
        if skill.lower() in tags:
            bold_strings += '<span class="font-weight-bold">%s</span> ' % (skill)
        else:
            normal_strings += '<span>%s</span> ' % (skill)

    return mark_safe("<p>%s %s</p>" % (bold_strings, normal_strings))
    