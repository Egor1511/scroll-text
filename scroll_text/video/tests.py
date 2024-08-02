import os
import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import ScrollingTextVideo


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ScrollingTextVideoModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_media = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_media)
        super().tearDownClass()

    def setUp(self):
        self.text = "Test scrolling text"
        self.video_file = SimpleUploadedFile("test_video.mp4", b"file_content",
                                             content_type="video/mp4")
        self.scrolling_text_video = ScrollingTextVideo.objects.create(
            text=self.text, video_file=self.video_file)

    def test_scrolling_text_video_creation(self):
        self.assertEqual(self.scrolling_text_video.text, self.text)
        self.assertTrue(self.scrolling_text_video.video_file.name.startswith(
            'video/videos/'))
        self.assertIsNotNone(self.scrolling_text_video.created_at)

    def test_string_representation(self):
        self.assertEqual(str(self.scrolling_text_video), self.text[:50])


class ScrollingTextVideoCreateDownloadViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('scroll_text')

    def test_missing_text_parameter(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_video_creation_and_download(self):
        text = "тестовый текст"
        response = self.client.get(self.url, {'text': text})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content_disposition = response.get('Content-Disposition')
        self.assertIn('attachment', content_disposition)
        self.assertIn('.mp4', content_disposition)

        self.assertTrue(ScrollingTextVideo.objects.filter(text=text).exists())
        video_record = ScrollingTextVideo.objects.get(text=text)
        self.assertTrue(os.path.exists(
            os.path.join(settings.MEDIA_ROOT, video_record.video_file.name)))

    def tearDown(self):
        for video in ScrollingTextVideo.objects.all():
            video.video_file.delete()
        ScrollingTextVideo.objects.all().delete()
