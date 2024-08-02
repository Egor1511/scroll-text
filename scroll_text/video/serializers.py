from rest_framework import serializers
from .models import ScrollingTextVideo


class ScrollingTextVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrollingTextVideo
        fields = ['id', 'text', 'video_file', 'created_at']
