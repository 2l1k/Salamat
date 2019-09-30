
from django import template
from brands.models import Brand

register = template.Library()


@register.inclusion_tag('brands/tags/brands.html', takes_context=True)
def get_brands(context):
    context['objects'] = Brand.objects.published()

    return context
