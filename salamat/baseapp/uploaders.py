
from django.http import HttpResponse
from filesoup.base import uploader_view
from baseapp.helpers import add_watermark


class RedactorUploaderMixin(object):
    """
    """
    @uploader_view(r'redactor-files\.json$')
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

    @uploader_view(r'redactor\.js$')
    def redactor_js(self):
        """
        Additional script for Redactor.js integration.
        """
        script = """
        Salamat.contextData.redactorOptions = {imageGetJson: '%s', emptyHtml: ''};
        """
        script %= self.reverse('redactor_files', args=(self.namespace,
                               self.prefix))
        return HttpResponse(script, content_type='text/javascript')
