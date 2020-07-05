import cloudinary
import os
from cloudinary_storage.storage import RawMediaCloudinaryStorage


class CustomRawMediaCloudinaryStorage(RawMediaCloudinaryStorage):
    
    def _upload(self, name, content):
        options = {
            'use_filename': True,
            'resource_type': self._get_resource_type(name), 
            'tags': self.TAG,
            'unique_filename': False # This differs from lib default
        }
        folder = os.path.dirname(name)
        if folder:
            options['folder'] = folder
        return cloudinary.uploader.upload(content, **options)
