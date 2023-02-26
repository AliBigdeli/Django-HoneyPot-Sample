from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import Photo


class PhotoSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)

