
from django.db import models
from django.utils.timezone import now
from filesoup import settings
from filesoup.helpers import upload_to_dir_slot_file


__all__ = ('BaseFile', 'SlotFile')


class BaseFile(models.Model):
    """
    Base file model.
    """
    file = models.FileField(max_length=255, upload_to=upload_to_dir_slot_file)
    name = models.CharField(max_length=255)
    date = models.DateTimeField(default=now)

    class Meta:
        abstract = True
        ordering = ('date',)

    def __unicode__(self):
        return self.name or self.file.name


class SlotFile(BaseFile):
    """
    A file model with virtual folder to save uploaded files to.
    """
    folder = models.CharField(max_length=255, db_index=True)
