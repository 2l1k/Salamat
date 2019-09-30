# coding=utf-8

from django.views.generic import ListView, DetailView
from news.models import News


class BaseNewsLisView(ListView):
    model = News

    def get_queryset(self):
        qs = News.objects.published()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(BaseNewsLisView, self).get_context_data(**kwargs)
        return ctx


class NewsListView(BaseNewsLisView):
    template_name = 'news/news.html'

    # def dispatch(self, request, *args, **kwargs):
    #     return super(
    #         ProjectListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(NewsListView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(NewsListView, self).get_context_data(**kwargs)

        return ctx


class NewsDetailView(DetailView):
    """ Project detail view in template project_detail.html"""
    template_name = 'news/news_detail.html'
    model = News

    def get_context_data(self, **kwargs):
        ctx = super(NewsDetailView, self).get_context_data(**kwargs)
        return ctx
