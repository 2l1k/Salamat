# coding=utf-8
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from rents.models import Rent

class RentListView(ListView):
    model = Rent

    def dispatch(self, request, *args, **kwargs):
        self.subject = None
        subject = request.GET.get('subject')
        if subject:
            try:
                self.subject = int(subject.split('-')[-1])
            except Exception, e:
                print e
                self.subject = None
        return super(RentListView, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        qs = Rent.objects.published()
        if self.subject:
            qs = qs.filter(building=self.subject)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(RentListView, self).get_context_data(**kwargs)
        ctx['cat1'] = self.get_queryset().filter(category=1)
        ctx['cat2'] = self.get_queryset().filter(category=2)
        return ctx

class RentDetailView(DetailView):
    """ Project detail view in template project_detail.html"""
    template_name = 'rents/rent_detail.html'
    model = Rent

    def get_context_data(self, **kwargs):
        ctx = super(RentDetailView, self).get_context_data(**kwargs)
        return ctx
