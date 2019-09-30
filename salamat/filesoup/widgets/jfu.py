
import mimetypes
import itertools

from django.forms.widgets import Media

from filesoup.widgets import UploaderWidget
from filesoup.utils import classproperty, cachedproperty


__all__ = ('JFUWidget',)


class JFUWidget(UploaderWidget):
    """
    A Jquery-File-Upload widget (Light).
    """
    template_name = 'filesoup/widgets/jfu/widget.html'
    file_upload_template_name = 'filesoup/widgets/jfu/file_upload.html'
    file_template_name = 'filesoup/widgets/jfu/file.html'

    # jQuery path to include. May be False or None to not include it.
    jquery = 'filesoup/jquery-1.8.2.min.js'

    # Default options.
    auto_upload = True
    sequential_uploads = True

    # Misc options.
    thumbnail_css_class = 'thumbnail'
    thumbnail_attrs = ''

    @classproperty
    def css_class(cls):
        """
        Widget container css classing.
        """
        if cls.uploader_class.ismultiple:
            return 'grid-layout well'

        return 'grid-layout well'

    @cachedproperty
    def meta(self):
        options = {
            'minFileSize': self.uploader.min_file_size,
            'maxFileSize': self.uploader.max_file_size,
            'maxNumberOfFiles': self.uploader.max_num,
            'autoUpload': self.auto_upload,
            'sequentialUploads': self.sequential_uploads,
        }

        # Determine `acceptFileTypes` option.
        allowed_exts = (mimetypes.guess_all_extensions(t)
                        for t in self.uploader.allowed_content_types)
        allowed_exts = itertools.chain.from_iterable(allowed_exts)
        allowed_exts_regexp = '|'.join(allowed_exts).replace('.', '')
        options['acceptFileTypes'] = r'/(\.|\/)(%s)$/i' % allowed_exts_regexp

        initializer = '$.filesoup.JFUSingleUploader'
        if self.uploader_class.ismultiple:
            initializer = '$.filesoup.JFUMultiUploader'

        return {
            'initializer': initializer,
            'options': options
        }

    @property
    def media(self):
        base_path = 'filesoup/widgets/jfu/jquery-file-upload-7.2.1/'

        js = [
            '%sjs/vendor/jquery.ui.widget.js' % base_path,
            '%sjs/jquery.iframe-transport.js' % base_path,
            '%sjs/jquery.fileupload.js' % base_path,
            '%sjs/jquery.fileupload-fp.js' % base_path,
            '%sjs/jquery.fileupload-ui.js' % base_path,
            '%sjs/cors/jquery.xdr-transport.js' % base_path,
            'filesoup/widgets/jfu/custom/js/uploader.js',
            'filesoup/widgets/jfu/custom/js/init.js'
        ]

        css = {
            'all': (
                'filesoup/widgets/jfu/custom/css/main.css',
            )
        }

        if self.jquery:
            js.insert(0, self.jquery)

        return Media(js=js, css=css)

    @property
    def admin_media(self):
        css = {
            'all': (
                'filesoup/widgets/jfu/custom/css/admin.css',
            )
        }

        return self.media['js'] + Media(css=css)
