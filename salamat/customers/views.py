# coding=utf-8

import json
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import UpdateView, TemplateView, ListView, DetailView, CreateView
from userena import settings as userena_settings
from userena.decorators import secure_required

from filesoup.mixins import RequestProvidingFormViewMixin

from catalog.models import Product, ProductCategory

from customers.models import Customer, Review, ClickHistory
from customers.forms import CustomerForm, ReviewForm


class CustomerDetailView(DetailView):
    """ Display all published products in template product_list.html"""

    template_name = 'customers/company.html'
    model = Customer
    pk_url_kwarg = 'pk'
    # def dispatch(self, request, *args, **kwargs):
    #     return super(
    #         ProductListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(CustomerDetailView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(CustomerDetailView, self).get_context_data(**kwargs)
        ctx['products'] = self.object.products[:16]
        cat_ids = self.object.products.values_list('category', flat=True)
        customer_ids_list = Product.objects.published().filter(
            category_id__in=cat_ids).values_list('user__profile__id', flat=True)
        customer_ids_list = list(set(customer_ids_list))
        ctx['similar_shops'] = Customer.objects.published().filter(
            id__in=customer_ids_list).order_by('?').exclude(id=self.object.id)[:8]
        if not ctx['similar_shops']:
            ctx['similar_shops'] = Customer.objects.published().order_by('?')[:8]
        return ctx


class ReviewCreateView(RequestProvidingFormViewMixin, CreateView):
    form_class = ReviewForm
    model = Review
    template_name = 'customers/company.html'

    def dispatch(self, request, *args, **kwargs):
        self.customer = get_object_or_404(Customer, id=kwargs.pop('pk'))
        category_id = request.GET.get('category', None)
        self.category = None
        if category_id:
            try:
                self.category = ProductCategory.objects.get(id=category_id)
            except ProductCategory.DoesNotExist:
                pass
        return super(ReviewCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ReviewCreateView, self).get_context_data(**kwargs)
        ctx['object'] = self.customer
        products = self.customer.products
        if self.category:
            child_ids = []
            for o in self.category.childs.published():
                child_ids.append(o.id)
                for c in o.childs.published():
                    child_ids.append(c.id)
            child_ids.append(self.category.id)

            products = products.filter(category__in=child_ids)
        ctx['products'] = products
        cat_ids = self.customer.products.values_list('category', flat=True).distinct()
        customer_ids_list = Product.objects.published().filter(
            category_id__in=cat_ids).values_list('user__profile__id', flat=True)
        customer_ids_list = list(set(customer_ids_list))
        ctx['similar_shops'] = Customer.objects.published().filter(
            id__in=customer_ids_list).order_by('?').exclude(id=self.customer.id)[:8]
        if not ctx['similar_shops']:
            ctx['similar_shops'] = Customer.objects.published().order_by('?')[:8]
        ctx['reviews'] = self.customer.shop_reviews.filter(active=True)
        cats = ProductCategory.objects.filter(id__in=cat_ids)
        cat_list = set([c.root for c in cats])

        ctx['categories'] = cat_list
        ctx['category'] = self.category
        return ctx

    def get_form_kwargs(self):
        kwargs = super(ReviewCreateView, self).get_form_kwargs()
        kwargs.update({'customer': self.customer})
        return kwargs

    def get_success_url(self):
        return self.customer.url

    def form_valid(self, form):
        messages.success(self.request, _(u'Отзыв добавлен'))
        return super(ReviewCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, u'Заполните поля корректно')
        return super(ReviewCreateView, self).form_invalid(form)


@secure_required
@login_required
def me(request):
    """
    User's home.
    """
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/me/')

    return render(request, 'customers/cabinet.html', {
        'profile': profile,
        'tab': int(request.GET.get('tab', 1))
    })

#
# class CustomerListView(ListView):
#     model = Customer
#
#     def get_queryset(self):
#         qs = Customer.objects.popular().filter(privacy='open')
#         return qs


class PlanView(TemplateView):
    template_name = 'plan.html'

    def get_context_data(self, **kwargs):
        ctx = super(PlanView, self).get_context_data(**kwargs)
        ctx['customers'] = Customer.objects.filter(privacy='open', building__isnull=False,
                                                   floor__isnull=False, apartment__isnull=False)
        customer_pk = self.request.GET.get('pk', None)
        if customer_pk:
            try:
                ctx['object'] = Customer.objects.get(pk=customer_pk)
            except Customer.DoesNotExist:
                pass
        return ctx


def show_phone(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer', None)
        if customer_id:
            customer = get_object_or_404(Customer, id=customer_id)
            customer.click_phone(request)
            return HttpResponse(json.dumps(dict(status=True)), content_type='json')
        else:
            return HttpResponse(json.dumps(dict(status=False)), content_type='json')
    else:
        raise Http404
