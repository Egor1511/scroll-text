# video/urls.py
from django.urls import path

from .views import ScrollingTextVideoCreateDownloadView

urlpatterns = [
    path('scroll-text/', ScrollingTextVideoCreateDownloadView.as_view(),
         name='scroll_text'),
]
