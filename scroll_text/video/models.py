from django.db import models


def generate_video_path(instance, filename: str) -> str:
    return f'video/videos/{filename}'


class ScrollingTextVideo(models.Model):
    text = models.TextField(
        verbose_name='Text'
    )
    video_file = models.FileField(
        upload_to=generate_video_path,
        verbose_name='Video File',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Scrolling Text Video'
        verbose_name_plural = 'Scrolling Text Videos'

    def __str__(self):
        return self.text[:50]


