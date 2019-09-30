# coding=utf-8

from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.contrib import messages
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http.response import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin

from filesoup.mixins import RequestProvidingFormViewMixin

from catalog.models import Product, ProductCategory, ProductCharacteristic, Review
from catalog.forms import (ProductForm, ProductUpdateForm, ProductCharacteristicForm, ProductSeoUpdateForm,
                           ReviewForm, SearchForm, ProductDiscountUpdateForm)


class BaseProductLisView(ListView):
    model = Product

    def get_queryset(self):
        qs = Product.objects.published()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(BaseProductLisView, self).get_context_data(**kwargs)
        return ctx


class ProductSearchView(BaseProductLisView):
    template_name = 'catalog/product_list.html'
    search = ''
    category = None

    def get_queryset(self):
        qs = super(ProductSearchView, self).get_queryset()
        self.form = SearchForm(self.request.GET)
        if self.form.is_valid():
            self.category = self.form.cleaned_data.get('categories', None)
            if self.category:
                child_ids = []
                for o in self.category.childs.published():
                    child_ids.append(o.id)
                    for c in o.childs.published():
                        child_ids.append(c.id)
                child_ids.append(self.category.id)

                qs = qs.filter(category__in=child_ids)
            self.search = self.form.cleaned_data.get('search', None)
            qs = qs.filter(title__icontains=self.search)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(ProductSearchView, self).get_context_data(**kwargs)
        ctx['products'] = self.get_queryset()
        ctx['search'] = self.search
        ctx['search_category'] = self.category
        return ctx


class CategoryDetailView(DetailView):
    """ Display all published products in template product_list.html"""

    template_name = 'catalog/product_list.html'
    model = ProductCategory
    slug_url_kwarg = 'category_slug'
    pk_url_kwarg = 'category_pk'
    # def dispatch(self, request, *args, **kwargs):
    #     return super(
    #         ProductListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(CategoryDetailView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(CategoryDetailView, self).get_context_data(**kwargs)
        child_ids = []
        for o in self.object.childs.published():
            child_ids.append(o.id)
            for c in o.childs.published():
                child_ids.append(c.id)
        child_ids.append(self.object.id)
        ctx['products'] = Product.objects.published().filter(category__in=child_ids)
        return ctx


class ProductDetailView(RequestProvidingFormViewMixin, DetailView):
    """ Product detail view in template product_detail.html"""

    template_name = 'catalog/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        ctx = super(ProductDetailView, self).get_context_data(**kwargs)
        ctx['tab'] = self.request.GET.get('tab', '1')
        ctx['review_form'] = ReviewForm( request=self.request)
        return ctx

    # def form_valid(self, form):
    #     messages.success(self.request, _(u'Товар добавлен'))
    #     return super(ProductDetailView, self).form_valid(form)
    #
    # def form_invalid(self, form):
    #     messages.error(self.request, u'Заполните поля корректно')
    #     return super(ProductDetailView, self).form_invalid(form)


class ProductCreateView(LoginRequiredMixin, RequestProvidingFormViewMixin, CreateView):
    form_class = ProductForm
    model = Product
    template_name = 'catalog/add_product.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            if self.request.user.profile.privacy != 'open':
                raise Http404
        except:
            raise Http404
        return super(ProductCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.url_update


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, id=kwargs.pop('pk'))
        return super(ProductDeleteView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(ProductDeleteView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get(self, request, *args, **kwargs):
        return super(ProductDeleteView, self).delete(request, *args, **kwargs)


    def get_success_url(self):
        return '%s?tab=3' % reverse('me')


class ProductUpdateView(LoginRequiredMixin, RequestProvidingFormViewMixin, UpdateView):
    form_class = ProductUpdateForm
    model = Product
    template_name = 'catalog/product_update.html'

    def get_context_data(self, **kwargs):
        ctx = super(ProductUpdateView, self).get_context_data(**kwargs)
        ctx['product'] = self.object
        tab = self.request.POST.get('tab', '1') if self.request.method == 'POST' else self.request.GET.get('tab', '1')
        ctx['tab'] = tab
        print tab
        return ctx

    def get_object(self, queryset=None):
        obj = super(ProductUpdateView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return self.object.url_update

    def post(self, request, *args, **kwargs):
        return super(ProductUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, _(u'Товар изменен'))

        return super(ProductUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, u'Заполните поля корректно')
        return super(ProductUpdateView, self).form_invalid(form)


class ProductSeoUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProductSeoUpdateForm
    model = Product
    template_name = 'catalog/product_update.html'

    def get_context_data(self, **kwargs):
        ctx = super(ProductSeoUpdateView, self).get_context_data(**kwargs)
        ctx['product'] = self.object
        ctx['tab'] = '3'
        return ctx

    def get_object(self, queryset=None):
        obj = super(ProductSeoUpdateView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return '%s?tab=3' % self.object.url_seo_update


class ProductDiscountUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProductDiscountUpdateForm
    model = Product
    template_name = 'catalog/product_update.html'

    def get_context_data(self, **kwargs):
        ctx = super(ProductDiscountUpdateView, self).get_context_data(**kwargs)
        ctx['product'] = self.object
        ctx['tab'] = '4'
        return ctx

    def get_object(self, queryset=None):
        obj = super(ProductDiscountUpdateView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return '%s?tab=4' % self.object.url_discount_update


class ProductCharacteristicCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductCharacteristicForm
    model = ProductCharacteristic
    template_name = 'catalog/product_update.html'

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, id=kwargs.pop('product_pk'))
        if not self.product.user == self.request.user:
            raise Http404
        return super(ProductCharacteristicCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ProductCharacteristicCreateView, self).get_context_data(**kwargs)
        ctx['tab'] = '2'
        ctx['product'] = self.product
        return ctx

    def get_form_kwargs(self):
        kwargs = super(ProductCharacteristicCreateView, self).get_form_kwargs()
        kwargs.update({'product': self.product})
        return kwargs


class ProductCharacteristicDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductCharacteristic

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, id=kwargs.pop('product_pk'))
        return super(ProductCharacteristicDeleteView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(ProductCharacteristicDeleteView, self).get_object()
        if not obj.product.user == self.request.user:
            raise Http404
        return obj

    def get(self, request, *args, **kwargs):
        return super(ProductCharacteristicDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.url


class ReviewCreateView(LoginRequiredMixin, RequestProvidingFormViewMixin, CreateView):
    form_class = ReviewForm
    model = Review
    template_name = 'catalog/product_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, id=kwargs.pop('product_pk'))
        return super(ReviewCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ReviewCreateView, self).get_context_data(**kwargs)
        ctx['product'] = self.product
        ctx['review_form'] = ctx['form']
        ctx['tab'] = '3'
        return ctx

    def get_form_kwargs(self):
        kwargs = super(ReviewCreateView, self).get_form_kwargs()
        kwargs.update({'product': self.product})
        return kwargs

    def get_success_url(self):
        return '%s?tab=3' % self.product.url

    def form_valid(self, form):
        messages.success(self.request, _(u'Отзыв добавлен'))
        return super(ReviewCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, u'Заполните поля корректно')
        return super(ReviewCreateView, self).form_invalid(form)