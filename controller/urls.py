from django.urls import path

from .views import *


urlpatterns = [
    path('linkedInimport/', Analyze.as_view(), name='analyze'),
]