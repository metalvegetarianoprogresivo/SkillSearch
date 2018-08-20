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

    for object in queryset:
        if object.lower() in tags:
            bold_strings += '<span class="font-weight-bold">%s</span> ' % (
                object,
            )
        else:
            normal_strings += '<span>%s</span> ' % (object,)
    return mark_safe("<p>%s %s</p>" % (bold_strings, normal_strings))
