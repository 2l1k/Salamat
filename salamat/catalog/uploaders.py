
import re

from django import forms
from django.http import HttpResponse

from filesoup.base import InlineModelUploader, uploader_view

from baseapp.uploaders import RedactorUploaderMixin

from catalog.models import Product, ProductImage


class BaseUploadForm(forms.ModelForm):
    """
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(BaseUploadForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        return super(BaseUploadForm, self).save(commit)


class ProductImageUploadForm(BaseUploadForm):
    class Meta:
        model = ProductImage
        exclude = ()


class AdminProductImageUploader(RedactorUploaderMixin, InlineModelUploader):
    """
    Photo uploader for Model admin.
    """
    max_file_size = 8000000  # 8MB max.
    max_num = None
    form = ProductImageUploadForm

    class Widget:
        thumbnail_css_class = 'thumbnail fresco'
        jquery = False

    model = ProductImage
    parent_model = Product
    use_model_upload_to = True

    product_edit_re = re.compile(r'product-(\d+)/')

    @classmethod
    def get_init_kwargs(cls, request, args, kwargs):
        init_kwargs = super(AdminProductImageUploader, cls).get_init_kwargs(
            request, args, kwargs)

        # Determine current model.
        products = None
        match = cls.product_edit_re.search(request.path)
        if match:
            product_pk = match.group(1)
            try:
                products = Product.objects.get(pk=product_pk)
            except products.DoesNotExist:
                pass
            else:
                init_kwargs['instance'] = products

        return init_kwargs

    def redactor_files(self):
        files = []
        for form in self.formset:
            file_dict = {
                'thumb': form.file_meta['thumbnail_url'],
                'image': form.file_meta['url']
            }

            if 'name' in form.file_meta:
                file_dict['title'] = form.file_meta['name']

            files.append(file_dict)

        return files

    def get_form_kwargs(self, i):
        """
        Pass a request in order to request.user become available in a form.
        """
        return dict(request=self.request)


class ProductImageUploader(InlineModelUploader):
    model = ProductImage
    parent_model = Product
    form = ProductImageUploadForm
    max_file_size = 5 * 1024 * 1024  # 5MB max.
    max_num = 10

    product_edit_re = re.compile(r'product-(\d+)/')

    class Widget:
        template_name = 'catalog/image_upload_widget.html'
        thumbnail_css_class = 'thumbnail fresco'
        jquery = False

    def get_form_kwargs(self, i):
        """
        Pass a request in order to request.user become available in a form.
        """
        return dict(request=self.request)

    # @uploader_view(r'redactor-files\.json$')
    # def redactor_files(self):
    #     files = []
    #     for form in self.formset:
    #         file_dict = {
    #             'thumb': form.file_meta['thumbnail_url'],
    #             'image': form.file_meta['url']
    #         }
    #
    #         if 'name' in form.file_meta:
    #             file_dict['title'] = form.file_meta['name']
    #
    #         files.append(file_dict)
    #
    #     return files
    #
    # @uploader_view(r'setup\.js$')
    # def setup_js(self):
    #     """
    #     Additional script for Redactor.js integration.
    #     """
    #     script = """
    #     Salamat.contextData.redactorOptions = {imageGetJson: '%s'};
    #     """
    #     script %= self.reverse('redactor_files', args=(self.namespace,
    #                            self.prefix))
    #     return HttpResponse(script, content_type='text/javascript')
    #
    # @classmethod
    # def get_init_kwargs(cls, request, args, kwargs):
    #     init_kwargs = super(ProductImageUploader, cls).get_init_kwargs(
    #         request, args, kwargs)
    #
    #     # Determine current product.
    #     product = None
    #     match = cls.product_edit_re.search(request.path)
    #     if match:
    #         product_pk = match.group(1)
    #         try:
    #             product = Product.objects.get(pk=product_pk)
    #         except Product.DoesNotExist:
    #             pass
    #         else:
    #             init_kwargs['instance'] = product
    #
    #     return init_kwargs
