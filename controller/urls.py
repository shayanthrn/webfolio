from django.urls import path
from controller.admin import Login_site
from .views import *


urlpatterns = [
    path('',dashboard.as_view(),name="dashboard"),
    path('login/',Login.as_view()),
    path('register/',Register.as_view()),
    path('dashboard/',dashboard.as_view()),
    path('import/',importv.as_view()),
    path('information/',information.as_view()),
    path('education/',education.as_view()),
    path('education/add/',addeducation.as_view()),
    path('work/',work.as_view()),
    path('work/add/',addwork.as_view()),
    path('portfolio/',portfolio.as_view()),
    path('portfolio/add/',addportfolio.as_view()),
    path('export/',export.as_view()),
    path('feedback/',feedback.as_view()),
]