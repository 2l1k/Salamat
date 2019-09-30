# coding=utf-8

from django.views.generic import ListView, DetailView
from projects.models import Project


class BaseProjectLisView(ListView):
    model = Project

    def get_queryset(self):
        qs = Project.objects.published()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(BaseProjectLisView, self).get_context_data(**kwargs)
        return ctx


class ProjectListView(BaseProjectLisView):
    """ Display all published projects in template project_list.html"""

    # def dispatch(self, request, *args, **kwargs):
    #     return super(
    #         ProjectListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(ProjectListView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(ProjectListView, self).get_context_data(**kwargs)
        return ctx


class ProjectListAllView(ProjectListView):
    """ Display all published projects in template all_project_list.html"""
    template_name = 'projects/all_project_list.html'


class ProjectDetailView(DetailView):
    """ Project detail view in template project_detail.html"""
    model = Project

    def get_context_data(self, **kwargs):
        ctx = super(ProjectDetailView, self).get_context_data(**kwargs)
        return ctx


class ProjectDetaiMobilelView(ProjectDetailView):
    template_name = ''