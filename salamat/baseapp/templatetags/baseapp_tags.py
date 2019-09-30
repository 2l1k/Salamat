
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import escape

# from baseapp.adminsite import get_applabel_display
from baseapp.helpers import get_absolute_url, add_watermark


register = template.Library()


@register.filter
def money_format(value):
    try:
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
    except Exception:
        return value

@register.filter
@stringfilter
def wraptag(value, tag):
    return mark_safe(u'<%(tag)s>%(value)s</%(tag)s>' % {'value': escape(value),
                                                        'tag': tag})


@register.filter
def mul(value, k):
    """
    Multiple value k times.
    """
    def numeric(s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    # Coerse to string to prevent localizing of value in template.
    return '%s' % (numeric(value) * numeric(k))


@register.simple_tag(takes_context=True)
def absolute_url(context, value):
    request = context.get('request', None)
    if request:
        return request.build_absolute_uri(value)
    return get_absolute_url(value)


# @register.filter
# @stringfilter
# def admin_applabel(applabel):
#     return get_applabel_display(applabel)


@register.filter
@stringfilter
def watermark(url):
    return add_watermark(url)


@register.filter
@stringfilter
def alert_css_class(message_tags):
    css_classes = []
    tag_constants = ['debug', 'info', 'success', 'warning', 'error']

    for tag in message_tags.split():
        if tag in tag_constants:
            css_classes.append('alert-%s' % tag)
        else:
            css_classes.append(tag)

    return ' '.join(css_classes)
