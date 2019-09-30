
from django import template
from catalog.models import ProductCategory
from customers.models import Customer

register = template.Library()


@register.filter
def money_format(value):
    value_str = str(value)
    fraction = ''

    if '.' in value_str:
        whole, fraction = value_str.split('.')
        if int(fraction) == 0:
            fraction = ''
    else:
        whole = value_str

    whole_len = len(whole)
    first_digits_count = whole_len % 3
    result = whole[:first_digits_count]
    for i in range(whole_len / 3):
        start = first_digits_count + (i * 3)
        result += ' ' + whole[start:start + 3]
    if fraction:
        result += '.' + fraction
    return result.strip()

@register.inclusion_tag('catalog/tags/catalog.html', takes_context=True)
def get_categories(context):
    context['cats'] = ProductCategory.objects.published().filter(parent__isnull=True)
    return context


@register.inclusion_tag('catalog/tags/categories.html', takes_context=True)
def get_parent_categories(context):
    context['cats'] = ProductCategory.objects.published().filter(parent__isnull=True)
    return context

@register.inclusion_tag('catalog/tags/categories_slider.html', takes_context=True)
def get_categories_slider(context):
    context['cats'] = ProductCategory.objects.published().filter(parent__isnull=True)
    return context


@register.inclusion_tag('catalog/tags/categories_field.html', takes_context=True)
def get_categories_field(context, val, title):
    context['cats'] = ProductCategory.objects.published().filter(parent__isnull=True)
    context['val'] = val
    context['title'] = title
    return context


@register.inclusion_tag('catalog/tags/filter_category.html', takes_context=True)
def get_filter_category(context):
    context['cats'] = ProductCategory.objects.published().filter(parent__isnull=True)
    context['companies'] = Customer.objects.published()
    # ProductCategory.objects.annotate(id=Customer('category'))
    return context