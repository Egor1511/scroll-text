import os

from django.core.files import File
from django.db import transaction
from django.http import FileResponse, HttpResponseBadRequest
from rest_framework.views import APIView

from .models import ScrollingTextVideo
from .scroll_text_video_generator import ScrollingTextVideoGenerator


class ScrollingTextVideoCreateDownloadView(APIView):
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        text = request.GET.get('text')
        if not text:
            return HttpResponseBadRequest("Missing 'text' parameter")

        video_generator = ScrollingTextVideoGenerator(
            text=text,
            duration=3,
            size=(100, 100),
            fps=24,
            text_color=(0, 0, 0),
            background_color=(170, 255, 195)
        )
        video_path = video_generator.create_video()
        with open(video_path, 'rb') as video_file:
            video = ScrollingTextVideo(
                text=text,
                video_file=File(video_file, name=os.path.basename(video_path))
            )
            video.save()

        return FileResponse(open(video_path, 'rb'), as_attachment=True,
                            filename=video_path)
