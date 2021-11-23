from base64 import b64decode
from uuid import uuid4

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):

    def to_representation(self, value):
        return value.url

    def to_internal_value(self, data):
        try:
            prefix, imagestr = data.split(';base64,')
            extension = '.' + prefix.split('/')[-1]
            extension = extension if extension != '.jpeg' else '.jpg'
            imagestr = b64decode(imagestr)
        except TypeError:
            raise TypeError('Image type is wrong')
        file_name = str(uuid4())[:12] + extension
        data = ContentFile(imagestr, name=file_name)

        return super().to_internal_value(data)
