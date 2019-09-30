
from django import template
from projects.models import Project

register = template.Library()


@register.inclusion_tag('projects/tags/projects.html', takes_context=True)
def get_projects(context):
    context['objects'] = Project.objects.published()
    return context

@register.inclusion_tag('projects/tags/recent_projects.html', takes_context=True)
def get_recent_projects(context):
    context['objects'] = Project.objects.published()
    return context