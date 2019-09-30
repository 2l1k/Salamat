
from django import template
from news.models import News

register = template.Library()


@register.inclusion_tag('news/tags/recent_news.html', takes_context=True)
def get_recent_news(context):
    context['news_list'] = News.objects.published()[:3]
    return context
