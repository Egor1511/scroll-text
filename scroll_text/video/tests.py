import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

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
