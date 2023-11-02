from django.urls import path
from controller.admin import Login_site
from .views import *


urlpatterns = [
    path('login/',Login_site.urls,name="login"),
    path('dashboard/',dashboard.as_view()),
    path('information/',information.as_view()),
    path('education/',education.as_view()),
    path('work/',work.as_view()),
    path('addwork/',addwork.as_view()),
    path('portfolio/',portfolio.as_view()),
    path('portfolio/add/',addportfolio.as_view()),
    path('export/',export.as_view()),
    path('feedback/',feedback.as_view()),
    path('test/', Test.as_view(), name='test'),
]