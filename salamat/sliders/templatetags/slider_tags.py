
from django import template
from sliders.models import Slider
from rents.models import Rent

register = template.Library()


@register.inclusion_tag('sliders/tags/sliders.html', takes_context=True)
def get_sliders(context):
    context['objects'] = Slider.objects.published().filter(place=1)
    context['rents'] = Rent.objects.published()
    return context


@register.inclusion_tag('sliders/tags/gallery_sliders.html', takes_context=True)
def get_gallery_slider(context):
    context['objects'] = Slider.objects.published().filter(place=2)
    return context


@register.inclusion_tag('sliders/tags/video_sliders.html', takes_context=True)
def get_video_slider(context):
    context['objects'] = Slider.objects.published().filter(place=3)
    return context