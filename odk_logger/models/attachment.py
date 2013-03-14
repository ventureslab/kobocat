import os
import mimetypes

from django.core.files.storage import get_storage_class
from django.db import models

from instance import Instance
from utils.image_tools import get_dimensions, resize


def upload_to(instance, filename):
    return os.path.join(
        instance.instance.user.username,
        'attachments',
        os.path.split(filename)[1])


class Attachment(models.Model):
    instance = models.ForeignKey(Instance, related_name="attachments")
    media_file = models.FileField(upload_to=upload_to)
    mimetype = models.CharField(
        max_length=20, null=False, blank=True, default='')

    class Meta:
        app_label = 'odk_logger'

    def save(self, *args, **kwargs):
        if self.media_file and self.mimetype == '':
            # guess mimetype
            mimetype, encoding = mimetypes.guess_type(self.media_file.name)
            if mimetype:
                self.mimetype = mimetype
        super(Attachment, self).save(*args, **kwargs)

