
import re
from filesoup.base import InlineModelUploader

from baseapp.uploaders import RedactorUploaderMixin
from projects.models import Project, ProjectImage


class AdminProjectImageUploader(RedactorUploaderMixin, InlineModelUploader):
    """
    Photo uploader for Model admin.
    """
    max_file_size = 8000000  # 8MB max.
    max_num = None

    class Widget:
        thumbnail_css_class = 'thumbnail fresco'
        jquery = False

    model = ProjectImage
    parent_model = Project
    use_model_upload_to = True

    project_edit_re = re.compile(r'project-(\d+)/')

    @classmethod
    def get_init_kwargs(cls, request, args, kwargs):
        init_kwargs = super(AdminProjectImageUploader, cls).get_init_kwargs(
            request, args, kwargs)

        # Determine current model.
        projects = None
        match = cls.project_edit_re.search(request.path)
        if match:
            project_pk = match.group(1)
            try:
                projects = Project.objects.get(pk=project_pk)
            except projects.DoesNotExist:
                pass
            else:
                init_kwargs['instance'] = projects

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
