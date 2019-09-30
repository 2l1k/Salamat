
from django import template
from notifications.models import Notification

register = template.Library()


@register.inclusion_tag('notifications/tags/notifications.html', takes_context=True)
def get_recent_notifications(context):
    context['objects'] = Notification.objects.published()
    return context
