from django.urls import path

from .views import *


urlpatterns = [
    path('linkedInimport/', Analyze.as_view(), name='analyze'),
    path('test/', Test.as_view(), name='test'),
]