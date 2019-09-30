
from django import template
from customers.models import Customer

register = template.Library()


@register.inclusion_tag('customers/tags/recent_customers.html', takes_context=True)
def get_recent_customers(context):
    context['customers_list'] = Customer.objects.published().order_by('id')

    return context